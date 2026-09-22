import logging
from typing import Optional

import jukebox
import jukebox.registry as registry
from jukebox.publishing.bus import EventBus

logger = logging.getLogger('jb.pub')

_BUS = EventBus()


def get_bus() -> EventBus:
    """The shared, thread-safe event bus. Prefer get_publisher() for the send/resend API."""
    return _BUS


class Publisher:
    """Thin, source-compatible wrapper around the shared :class:`EventBus`.

    Kept as a class only so existing call sites (``publishing.get_publisher().send(...)``) don't
    need to change. Unlike the old ZMQ-backed Publisher, a single shared instance is safe to use
    from any thread -- the "one Publisher per thread" rule from the ZMQ days is gone along with
    ZMQ (see documentation/developers/roadmap-core-architecture.md).
    """

    def send(self, topic: str, payload) -> None:
        """Send out a message for topic"""
        _BUS.publish(topic, payload)

    def revoke(self, topic: str) -> None:
        """Revoke a single topic element (not a topic tree!)"""
        _BUS.publish(topic, None)

    def resend(self, topic: Optional[str] = None) -> None:
        """Re-send current status of the topic tree `topic` (default: everything) to all subscribers.

        Not necessary to call after incremental updates or new subscriptions -- that happens
        automatically."""
        _BUS.resend(topic or '')

    def close_server(self) -> None:
        """No-op, kept for source compatibility with the old shutdown call.

        There is no separate server thread to close down anymore -- the bus is just an object."""


_PUBLISHER = Publisher()


def get_publisher() -> Publisher:
    """Return the shared publisher instance.

    Example::

        import jukebox.publishing as publishing
        publishing.get_publisher().send('hello', f'Hi there, howya?')
    """
    return _PUBLISHER


def republish(topic=None):
    """Re-publish the topic tree 'topic' to all subscribers

    :param topic: Topic tree to republish. None = resend all"""
    get_publisher().resend(topic)


def register():
    registry.register(republish, name='republish', package='publishing')


def start():
    get_publisher().send('core.welcome', 'Welcome! Let the sound begin')
    get_publisher().send('core.version', jukebox.version())


def stop(**ignored_kwargs):
    logger.debug("Closing publisher")
    get_publisher().send('core.welcome', 'Goodbye. Hear you later!')
