from typing import Optional

from jukebox.publishing.bus import EventBus

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
        """No-op, kept for source compatibility with components/publishing's shutdown call.

        There is no separate server thread to close down anymore -- the bus is just an object."""


_PUBLISHER = Publisher()


def get_publisher() -> Publisher:
    """Return the shared publisher instance.

    Example::

        import jukebox.publishing as publishing
        publishing.get_publisher().send('hello', f'Hi there, howya?')
    """
    return _PUBLISHER
