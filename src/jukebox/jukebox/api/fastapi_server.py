# -*- coding: utf-8 -*-
"""FastAPI + uvicorn HTTP and WebSocket API server.

Reimplements the Tornado-based bridge (`jukebox.api.server`) endpoint-by-endpoint on FastAPI/uvicorn,
per documentation/developers/roadmap-core-architecture.md step 2. Runs side by side with the Tornado
server for now: nothing outside this module references it yet, and it is not wired into the daemon.

Covers the same first slice as the Tornado bridge did before its library endpoints were added:
health, RPC passthrough, and events-over-websocket. Library endpoints are step 3 of the roadmap.

The RPC executor here is sized for concurrency rather than serialized to one worker like the Tornado
version: `jukebox.plugs.call()` already serializes every dispatched call behind its own module-level
lock (see `_lock_module` in `jukebox/plugs.py`), so multiple executor workers only let independent
requests (e.g. concurrent health checks, or RPC calls queued behind a slow hardware call) be picked up
without blocking each other at the HTTP layer -- they still serialize at the plugin-dispatch layer,
same as before.
"""

import asyncio
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

import uvicorn
import zmq
import zmq.asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.requests import Request

import jukebox.cfghandler
from jukebox.api.server import EventBroker, PUBLISH_ENDPOINT, parse_subscription_command
from jukebox.rpc.processor import process_request

logger = logging.getLogger('jb.api.fastapi_server')
cfg = jukebox.cfghandler.get_handler('jukebox')

RPC_EXECUTOR_WORKERS = 4


class _WebSocketClient:
    """Adapts a FastAPI WebSocket to the EventBroker's `write_message` / `subscriptions` contract."""

    def __init__(self, websocket: WebSocket, loop: asyncio.AbstractEventLoop):
        self._websocket = websocket
        self._loop = loop
        self.subscriptions = set()

    def write_message(self, message):
        return asyncio.run_coroutine_threadsafe(self._websocket.send_json(message), self._loop)


async def _handle_rpc_request(request: Request, executor, rpc_processor):
    content_type = request.headers.get('content-type', '')
    media_type = content_type.split(';', 1)[0].strip().lower()
    if media_type != 'application/json':
        return JSONResponse(status_code=400, content={'error': 'Content-Type must be application/json.'})

    body = await request.body()
    try:
        client_request = json.loads(body)
    except (ValueError, UnicodeDecodeError) as error:
        return JSONResponse(status_code=400, content={'error': f'Malformed JSON: {error}'})

    if not isinstance(client_request, dict):
        return JSONResponse(status_code=400, content={'error': 'RPC request must be an object.'})

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, rpc_processor, client_request)


async def _handle_events_websocket(websocket: WebSocket, broker):
    await websocket.accept()
    loop = asyncio.get_running_loop()
    client = _WebSocketClient(websocket, loop)
    broker.register(client)
    try:
        while True:
            command = await websocket.receive_json()
            try:
                command_type, topics = parse_subscription_command(command)
            except ValueError as error:
                await websocket.close(code=1008, reason=str(error))
                return
            if command_type == 'subscribe':
                broker.subscribe(client, topics)
            else:
                broker.unsubscribe(client, topics)
    except WebSocketDisconnect:
        pass
    finally:
        broker.unregister(client)


def create_app(broker, executor, rpc_processor=process_request):
    app = FastAPI()

    @app.get('/api/v1/health')
    async def health():
        return {'status': 'ok'}

    @app.post('/api/v1/rpc')
    async def rpc(request: Request):
        return await _handle_rpc_request(request, executor, rpc_processor)

    @app.websocket('/api/v1/events')
    async def events(websocket: WebSocket):
        await _handle_events_websocket(websocket, broker)

    return app


class FastApiServer(threading.Thread):
    """Run the browser API on an isolated asyncio event loop, mirroring `jukebox.api.server.ApiServer`."""

    def __init__(self, bind_address=None, port=None, context=None):
        super().__init__(name='FastApiServer', daemon=True)
        self.bind_address = bind_address or cfg.getn('api', 'bind_address', default='127.0.0.1')
        self.port = port if port is not None else cfg.getn('api', 'fastapi_port', default=5557)
        self.context = context or zmq.asyncio.Context.instance()
        self.broker = EventBroker()
        self._ready = threading.Event()
        self._startup_error = None
        self._loop = None
        self._server = None
        self._executor = None
        self._subscriber = None
        self._subscriber_task = None

    def start_and_wait(self, timeout=5):
        self.start()
        if not self._ready.wait(timeout):
            raise TimeoutError('Timed out while starting FastAPI server.')
        if self._startup_error is not None:
            raise RuntimeError('Could not start FastAPI server.') from self._startup_error

    def run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._run_async())
        except Exception as error:
            self._startup_error = error
            logger.exception("FastAPI server failed")
            self._ready.set()
        finally:
            self._loop.close()

    async def _run_async(self):
        self._executor = ThreadPoolExecutor(max_workers=RPC_EXECUTOR_WORKERS, thread_name_prefix='FastApiRpc')
        app = create_app(self.broker, self._executor)

        config = uvicorn.Config(app, host=self.bind_address, port=self.port, loop='none', log_config=None)
        self._server = uvicorn.Server(config)

        self._subscriber = self.context.socket(zmq.SUB)
        self._subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        self._subscriber.setsockopt(zmq.LINGER, 0)
        self._subscriber.connect(PUBLISH_ENDPOINT)
        self._subscriber_task = asyncio.ensure_future(self._subscriber_loop())

        serve_task = asyncio.ensure_future(self._server.serve())
        while not self._server.started and not serve_task.done():
            await asyncio.sleep(0.01)
        if serve_task.done() and serve_task.exception() is not None:
            raise serve_task.exception()

        logger.info(f"FastAPI server listening on {self.bind_address}:{self.port}")
        self._ready.set()
        try:
            await serve_task
        finally:
            self._subscriber_task.cancel()
            self._subscriber.close(linger=0)
            self._executor.shutdown(wait=False, cancel_futures=True)

    async def _subscriber_loop(self):
        try:
            while True:
                message = await self._subscriber.recv_multipart()
                self.broker.publish(message)
        except asyncio.CancelledError:
            pass

    def terminate(self, timeout=5):
        logger.info("Closing FastAPI server")
        if not self.is_alive():
            return
        self._ready.wait(timeout)
        if self._loop is not None and self._server is not None:
            self._loop.call_soon_threadsafe(self._request_shutdown)
        self.join(timeout)
        if self.is_alive():
            logger.warning("FastAPI server did not stop within the shutdown timeout")

    def _request_shutdown(self):
        self._server.should_exit = True
