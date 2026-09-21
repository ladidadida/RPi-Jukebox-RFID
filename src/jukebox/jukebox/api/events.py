# -*- coding: utf-8 -*-
"""Transport-neutral pieces of the browser events-over-websocket bridge.

Split out of the old Tornado bridge (`jukebox.api.server`, removed once `jukebox.api.fastapi_server`
became the sole HTTP/WebSocket bridge -- see documentation/developers/roadmap-core-architecture.md)
so nothing here depends on a specific web framework.
"""

import json
import logging

logger = logging.getLogger('jb.api.events')

MAX_MESSAGE_SIZE = 1024 * 1024
PUBLISH_ENDPOINT = 'inproc://PublisherToProxy'


class EventBroker:
    """Maintain browser subscriptions and a private last-value cache."""

    def __init__(self):
        self.cache = {}
        self.clients = set()

    def register(self, client):
        self.clients.add(client)

    def unregister(self, client):
        self.clients.discard(client)

    @staticmethod
    def _matches(topic, subscriptions):
        return any(topic.startswith(prefix) for prefix in subscriptions)

    def subscribe(self, client, topics):
        client.subscriptions.update(topics)
        for topic, data in self.cache.items():
            if self._matches(topic, topics):
                self._send(client, {
                    'type': 'event',
                    'topic': topic,
                    'data': data,
                })

    @staticmethod
    def unsubscribe(client, topics):
        client.subscriptions.difference_update(topics)

    def publish(self, message):
        if len(message) != 2:
            logger.warning(f"Ignoring malformed publisher message with {len(message)} parts")
            return

        topic_bytes, payload = message
        try:
            topic = topic_bytes.decode('utf-8')
        except UnicodeDecodeError as error:
            logger.warning(f"Ignoring publisher topic that is not UTF-8: {error}")
            return

        if payload == b'':
            self.cache.pop(topic, None)
            outgoing = {'type': 'revoke', 'topic': topic}
        else:
            try:
                data = json.loads(payload)
            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                logger.warning(f"Ignoring malformed publisher payload for '{topic}': {error}")
                return
            self.cache[topic] = data
            outgoing = {'type': 'event', 'topic': topic, 'data': data}

        for client in tuple(self.clients):
            if self._matches(topic, client.subscriptions):
                self._send(client, outgoing)

    def _send(self, client, message):
        try:
            future = client.write_message(message)
        except Exception:
            # Transport-neutral: covers any transport's synchronous "client is gone" signal.
            self.unregister(client)
            return

        if future is not None:
            future.add_done_callback(lambda completed: completed.exception())


def parse_subscription_command(command):
    """Validate a decoded events-websocket command.

    :return: ``(command_type, topics)``
    :raises ValueError: if the command is not a well-formed subscribe/unsubscribe request
    """
    if not isinstance(command, dict):
        raise ValueError('Commands must be objects.')

    command_type = command.get('type')
    topics = command.get('topics')
    if (
        command_type not in ('subscribe', 'unsubscribe')
        or not isinstance(topics, list)
        or any(not isinstance(topic, str) for topic in topics)
    ):
        raise ValueError('Invalid subscription command.')

    return command_type, topics
