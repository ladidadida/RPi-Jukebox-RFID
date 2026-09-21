#!/usr/bin/env python
"""
A command line tool that monitors all messages being sent out from the
Jukebox via the publishing interface. Received messages are printed in the console.
Mainly used for debugging.

Connects to the FastAPI events-over-websocket endpoint (see jukebox.api.fastapi_server) rather
than ZMQ pub/sub directly -- ZMQ was dropped as an internal transport, see
documentation/developers/roadmap-core-architecture.md ("Simplify away ZMQ and nginx").
"""
import argparse
import asyncio
import json
import logging

import misc.loggingext
import websockets

logger = misc.loggingext.configure_default(logging.WARNING)
topic_width = 40


async def main(url, topics):
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({'type': 'subscribe', 'topics': topics or ['']}))
        while True:
            message = json.loads(await websocket.recv())
            if message['type'] == 'revoke':
                print(f"{message['topic']:{topic_width}}: <revoked>")
            else:
                print(f"{message['topic']:{topic_width}}: {message['data']}")


if __name__ == '__main__':
    default_port = 5556
    argparser = argparse.ArgumentParser(
        description='The Jukebox Publisher sniffer tool',
        epilog=f'Default connection port: {default_port}\nExample:\n$ {__file__} -p 5556 -k core host',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    argparser.add_argument("-p", "--port",
                           help=f"Connect to the API server on PORT [default: {default_port}]",
                           type=int, default=default_port, metavar="PORT")

    argparser.add_argument('-k', '--topics', metavar='TOPIC',
                           help="Subscribe to this topic tree(s). If omitted all topics are subscribed.",
                           nargs='+',
                           default=None)
    args = argparser.parse_args()

    url = f"ws://localhost:{args.port}/api/v1/events"

    print(f">>> Sniffer Client connect on {url} for topics '{args.topics}'\n\n")

    try:
        asyncio.run(main(url, args.topics))
    except KeyboardInterrupt:
        pass

    print("\n\n>>> Sniffer Client exited!")
