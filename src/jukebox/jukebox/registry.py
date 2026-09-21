# -*- coding: utf-8 -*-
"""Explicit call registry for core components.

Replaces the old dynamic, config-driven plugin system (formerly ``jukebox.plugs``): components are
registered directly by ``daemon.py`` at start-up instead of being discovered from ``jukebox.yaml`` via
decorator magic (``@plugs.register`` / ``@plugs.initialize`` / ``@plugs.finalize`` / ``@plugs.atexit``).

There is no dynamic loading and no module-wide serializing lock here (the old ``plugs.py`` serialized
every call through one global lock regardless of which component it targeted -- see
documentation/developers/roadmap-core-architecture.md). Each component is responsible for its own
thread-safety.

Call addressing (``package``, ``plugin``, ``method``) is unchanged from the old system so the webapp's
RPC call shape (``{'package': ..., 'plugin': ..., 'method': ...}``) keeps working without changes on
that side.
"""

import logging
import threading
import traceback
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger('jb.registry')

_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register(obj: Any, name: str, package: str) -> Any:
    """Register ``obj`` (a function, bound method, or class instance) under ``package.name``."""
    _REGISTRY.setdefault(package, {})[name] = obj
    return obj


def unregister(package: str, name: Optional[str] = None) -> None:
    if name is None:
        _REGISTRY.pop(package, None)
    else:
        _REGISTRY.get(package, {}).pop(name, None)


def callable_method(func: Callable) -> Callable:
    """Mark a bound method as callable through the registry (i.e. over RPC)."""
    setattr(func, 'registry_callable', True)
    return func


# Kept as `tag` for drop-in compatibility with the many existing `@plugs.tag` call sites.
tag = callable_method


def exists(package: str, plugin: Optional[str] = None, method: Optional[str] = None) -> bool:
    if package not in _REGISTRY:
        return False
    if plugin is None:
        return True
    if plugin not in _REGISTRY[package]:
        return False
    if method is None:
        return True
    return hasattr(_REGISTRY[package][plugin], method)


def get(package: str, plugin: Optional[str] = None, method: Optional[str] = None) -> Any:
    if plugin is None:
        raise TypeError("Argument 'plugin' is mandatory")
    try:
        obj = _REGISTRY[package][plugin]
    except KeyError:
        raise NameError(f"Not registered: '{package}.{plugin}'")
    if method is None:
        return obj
    func = getattr(obj, method, None)
    if func is None:
        raise NameError(f"'{package}.{plugin}' has no attribute '{method}'")
    return func


def dereference(package: str, plugin: str, method: Optional[str] = None, *, args=None, kwargs=None):
    func = get(package, plugin, method)
    if args is None:
        args = ()
    elif isinstance(args, str):
        args = [args]
    else:
        try:
            args.__iter__()
        except AttributeError:
            args = [args]
    if kwargs is None:
        kwargs = {}
    if (not callable(func)):
        raise TypeError(f"Not callable: '{package}.{plugin}'" + (f".{method}" if method else ''))
    if method is not None and not getattr(func, 'registry_callable', False):
        raise TypeError(f"'{package}.{plugin}.{method}' is not tagged as callable")
    return func, args, kwargs


def call(package: str, plugin: str, method: Optional[str] = None, *,
         args=(), kwargs=None, as_thread: bool = False, thread_name: Optional[str] = None) -> Any:
    """Call a registered function/method. See the old ``jukebox.plugs.call`` for the historical
    behavioural contract this preserves (addressing, ``as_thread`` semantics)."""
    func, args, kwargs = dereference(package, plugin, method, args=args, kwargs=kwargs)
    if as_thread:
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True, name=thread_name)
        thread.start()
        return thread
    return func(*args, **kwargs)


def call_ignore_errors(package: str, plugin: str, method: Optional[str] = None, *,
                       args=(), kwargs=None, as_thread: bool = False, thread_name: Optional[str] = None) -> Any:
    """Like :func:`call`, but exceptions are logged and swallowed rather than propagated."""
    try:
        return call(package, plugin, method, args=args, kwargs=kwargs, as_thread=as_thread, thread_name=thread_name)
    except Exception as error:
        name = f'{package}.{plugin}' + (f'.{method}' if method else '')
        logger.error(f"Ignoring failed call: '{name}(args={args}, kwargs={kwargs})'")
        logger.error(f"Reason: {error.__class__.__name__}: {error}")
        logger.error(f"Detailed reason:\n{traceback.format_exc()}")
        return None


def dump_registry(stream):
    """Write a human readable summary of all registered callables to stream."""
    for package, plugins in _REGISTRY.items():
        print(f"Package: '{package}'", file=stream)
        for name, obj in plugins.items():
            print(f"    {name}: {obj!r}", file=stream)
