"""`jukebox plugin ...`: list installed plugins, enable/disable them in the configuration, install new ones."""

import shutil
import subprocess
import sys
from importlib.metadata import entry_points
from pathlib import Path
from typing import List, Optional

import typer

import jukebox.cfghandler
import jukebox.paths
from jukebox.contract.manager import ENTRY_POINT_GROUP

app = typer.Typer(help="Manage plugins.", no_args_is_help=True)

ConfOption = typer.Option(None, "-c", "--conf", envvar="JUKEBOX_CONF",
                          help="Jukebox configuration file (default: $JUKEBOX_HOME/settings/jukebox.yaml)")


def _config(conf: Optional[Path]):
    path = conf or jukebox.paths.settings_dir() / 'jukebox.yaml'
    jukebox.cfghandler.ensure_default_config(
        str(path), str(jukebox.paths.resource('default-settings', 'jukebox.default.yaml')))
    cfg = jukebox.cfghandler.ConfigHandler('plugin-cli')
    jukebox.cfghandler.load_yaml(cfg, str(path))
    return cfg, path


def _enabled(cfg) -> dict:
    plugins = cfg.getn('plugins', default=None)
    return plugins if isinstance(plugins, dict) else {}


def _installed():
    return {ep.name: ep for ep in entry_points(group=ENTRY_POINT_GROUP)}


def _load(ep):
    """(plugin class, None) or (None, reason it can't be imported)."""
    try:
        return ep.load(), None
    except Exception as error:
        return None, f"{error.__class__.__name__}: {error}"


def install_requirements(requirements: List[str]) -> None:
    """Install into the environment the jukebox runs in (uv if available, else pip)."""
    uv = shutil.which('uv')
    if uv:
        command = [uv, 'pip', 'install', '--python', sys.executable, *requirements]
    else:
        command = [sys.executable, '-m', 'pip', 'install', *requirements]
    typer.echo(f"$ {' '.join(command)}")
    subprocess.run(command, check=True)


@app.command('list')
def list_plugins(conf: Optional[Path] = ConfOption) -> None:
    """Installed plugins, whether they are enabled, and why one can't be loaded."""
    cfg, path = _config(conf)
    enabled = _enabled(cfg)
    installed = _installed()
    for name in sorted(set(installed) | set(enabled)):
        ep = installed.get(name)
        state = 'enabled ' if name in enabled else 'disabled'
        if ep is None:
            typer.echo(f"{state}  {name:24}  NOT INSTALLED")
            continue
        cls, problem = _load(ep)
        dist = f"{ep.dist.name} {ep.dist.version}" if ep.dist else ''
        summary = problem or ((cls.__doc__ or '').strip().split('\n', 1)[0])
        typer.echo(f"{state}  {name:24}  {dist:36}  {summary}")
    typer.echo(f"\n(configuration: {path})")


@app.command()
def enable(name: str, conf: Optional[Path] = ConfOption,
           with_extras: bool = typer.Option(False, "--with-extras",
                                            help="Install the dependencies the plugin declares as extras")) -> None:
    """Enable an installed plugin (takes effect on the next start)."""
    ep = _installed().get(name)
    if ep is None:
        typer.echo(f"Plugin '{name}' is not installed. Installed: {', '.join(sorted(_installed())) or 'none'}", err=True)
        raise typer.Exit(1)
    cls, problem = _load(ep)
    extras = tuple(getattr(cls, 'extras', ()) or ()) if cls is not None else ()
    if with_extras and extras and ep.dist is not None:
        install_requirements([f"{ep.dist.name}[{','.join(extras)}]"])
    elif extras:
        typer.echo(f"Note: '{name}' uses the extras {', '.join(extras)} of {ep.dist.name if ep.dist else 'its package'}; "
                   f"install them with --with-extras if they are missing.")
    if problem and not with_extras:
        typer.echo(f"Warning: '{name}' can't be loaded right now: {problem}", err=True)
    cfg, path = _config(conf)
    if name in _enabled(cfg):
        typer.echo(f"'{name}' is already enabled in {path}")
        return
    cfg.setndefault('plugins', name, value={})
    jukebox.cfghandler.write_yaml(cfg, str(path))
    typer.echo(f"Enabled '{name}' in {path}. Restart the jukebox to load it.")


@app.command()
def disable(name: str, conf: Optional[Path] = ConfOption) -> None:
    """Disable a plugin (its settings are removed from the configuration)."""
    cfg, path = _config(conf)
    enabled = _enabled(cfg)
    if name not in enabled:
        typer.echo(f"'{name}' is not enabled in {path}")
        return
    del enabled[name]
    if not enabled:
        cfg['plugins'] = {}
    jukebox.cfghandler.write_yaml(cfg, str(path))
    typer.echo(f"Disabled '{name}' in {path}. Restart the jukebox to unload it.")


@app.command()
def install(spec: str, conf: Optional[Path] = ConfOption,
            enable_plugins: bool = typer.Option(False, "--enable", help="Enable the plugins the package provides")) -> None:
    """Install a plugin package (a pip requirement, wheel file, URL or directory)."""
    before = set(_installed())
    install_requirements([spec])
    new = sorted(set(_installed()) - before)
    if not new:
        typer.echo("The package provides no new plugins (or they were installed already).")
        return
    typer.echo(f"New plugins: {', '.join(new)}")
    for name in new:
        if enable_plugins:
            enable(name, conf=conf, with_extras=False)
        else:
            typer.echo(f"  enable with: jukebox plugin enable {name}")
