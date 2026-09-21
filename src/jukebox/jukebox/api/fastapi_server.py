# -*- coding: utf-8 -*-
"""FastAPI + uvicorn HTTP and WebSocket API server.

The sole browser-facing HTTP/WebSocket bridge -- replaced the Tornado-based `jukebox.api.server`
(see documentation/developers/roadmap-core-architecture.md, steps 2-6). Serves health, RPC
passthrough, events-over-websocket, the library upload/folder/entries/refresh endpoints, and (see
jukebox.api.webapp_static) the webapp's static build + /logs -- nginx is gone, this is now the one
thing reachable from the LAN, hence `api.bind_address` defaulting to 0.0.0.0.

The RPC executor here is sized for concurrency rather than serialized to one worker like the Tornado
version was: unlike the old `jukebox.plugs` system this replaced, `jukebox.registry.call()` has no
shared global lock, so multiple executor workers actually buy real concurrency now -- each component
is responsible for its own thread-safety.
"""

import asyncio
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.requests import Request

import jukebox.cfghandler
import jukebox.publishing
from jukebox.api.events import EventBroker, MAX_MESSAGE_SIZE, parse_subscription_command
from jukebox.api.webapp_static import register_webapp_routes
from jukebox.library import LibraryError, MAX_UPLOAD_SIZE, create_music_library
from jukebox.rpc.processor import process_request

logger = logging.getLogger('jb.api.fastapi_server')
cfg = jukebox.cfghandler.get_handler('jukebox')

RPC_EXECUTOR_WORKERS = 4
LIBRARY_EXECUTOR_WORKERS = 1

# src/jukebox/jukebox/api/fastapi_server.py -> repo root is 4 levels up (matches the
# ../../shared/... convention src/jukebox/run_jukebox.py already uses for config paths).
_REPO_ROOT = Path(__file__).resolve().parents[4]


def default_webapp_build_dir() -> Path:
    return _REPO_ROOT / 'src' / 'webapp' / 'build'


def default_logs_dir() -> Path:
    return _REPO_ROOT / 'shared' / 'logs'


class _WebSocketClient:
    """Adapts a FastAPI WebSocket to the EventBroker's `write_message` / `subscriptions` contract."""

    def __init__(self, websocket: WebSocket, loop: asyncio.AbstractEventLoop):
        self._websocket = websocket
        self._loop = loop
        self.subscriptions = set()

    def write_message(self, message):
        return asyncio.run_coroutine_threadsafe(self._websocket.send_json(message), self._loop)


class _BodyTooLarge(Exception):
    """Raised by :func:`_read_limited_body` when the request body exceeds its size limit."""


async def _read_limited_body(request: Request, limit: int) -> bytes:
    """Read the request body, aborting as soon as it exceeds `limit` bytes.

    Mirrors the Tornado bridge's streaming size guard (`MAX_MESSAGE_SIZE`) instead of buffering an
    arbitrarily large body before checking its size.
    """
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > limit:
            raise _BodyTooLarge()
    return bytes(body)


async def _handle_rpc_request(request: Request, executor, rpc_processor):
    content_type = request.headers.get('content-type', '')
    media_type = content_type.split(';', 1)[0].strip().lower()
    if media_type != 'application/json':
        return JSONResponse(status_code=400, content={'error': 'Content-Type must be application/json.'})

    try:
        body = await _read_limited_body(request, MAX_MESSAGE_SIZE)
    except _BodyTooLarge:
        return JSONResponse(status_code=413, content={'error': 'Request body exceeds 1 MiB.'})
    try:
        client_request = json.loads(body)
    except (ValueError, UnicodeDecodeError) as error:
        return JSONResponse(status_code=400, content={'error': f'Malformed JSON: {error}'})

    if not isinstance(client_request, dict):
        return JSONResponse(status_code=400, content={'error': 'RPC request must be an object.'})

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, rpc_processor, client_request)


def _is_same_origin(websocket: WebSocket) -> bool:
    """Reject cross-origin WebSocket handshakes, matching Tornado's default `check_origin`.

    Without this, any page in the browser could open a WebSocket to this API and read (or, via
    future write-capable topics, trigger) whatever it exposes -- classic cross-site WebSocket
    hijacking. Starlette/FastAPI don't check this by default, unlike Tornado's WebSocketHandler.
    """
    origin = websocket.headers.get('origin')
    if origin is None:
        # Non-browser clients (e.g. the RPC CLI talking WS directly) don't send Origin at all.
        return True
    origin_host = urlsplit(origin).netloc.lower()
    request_host = (websocket.headers.get('host') or '').lower()
    return origin_host == request_host


async def _handle_events_websocket(websocket: WebSocket, broker):
    if not _is_same_origin(websocket):
        await websocket.close(code=1008)
        return
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


def _library_error_response(error: LibraryError) -> JSONResponse:
    return JSONResponse(
        status_code=error.status,
        content={'error': {'code': error.code, 'message': error.message}},
    )


async def _library_json_body(request: Request) -> dict:
    content_type = request.headers.get('content-type', '')
    media_type = content_type.split(';', 1)[0].strip().lower()
    if media_type != 'application/json':
        raise LibraryError(400, 'invalid_content_type', 'Content-Type must be application/json.')
    try:
        body = await _read_limited_body(request, MAX_MESSAGE_SIZE)
    except _BodyTooLarge:
        raise LibraryError(413, 'request_too_large', 'Request body exceeds 1 MiB.')
    try:
        parsed = json.loads(body)
    except (ValueError, UnicodeDecodeError) as error:
        raise LibraryError(400, 'invalid_json', f'Malformed JSON: {error}') from error
    if not isinstance(parsed, dict):
        raise LibraryError(400, 'invalid_request', 'The request body must be an object.')
    return parsed


def _reject_oversized_upload(request: Request):
    content_length = request.headers.get('content-length')
    if content_length is None:
        return None
    try:
        too_large = int(content_length) > MAX_UPLOAD_SIZE
    except ValueError:
        return None
    if not too_large:
        return None
    return JSONResponse(status_code=413, content={'error': {
        'code': 'file_too_large', 'message': 'Files are limited to 1 GiB.',
    }})


def _require_upload_query_params(request: Request):
    folder = request.query_params.get('folder')
    file_name = request.query_params.get('name')
    if folder is not None and file_name is not None:
        return folder, file_name, None
    missing = 'folder' if folder is None else 'name'
    error_response = JSONResponse(status_code=400, content={'error': {
        'code': 'invalid_request', 'message': f"Missing query parameter '{missing}'.",
    }})
    return None, None, error_response


async def _handle_library_upload(request: Request, library, executor):
    oversized_response = _reject_oversized_upload(request)
    if oversized_response is not None:
        return oversized_response

    folder, file_name, error_response = _require_upload_query_params(request)
    if error_response is not None:
        return error_response

    loop = asyncio.get_running_loop()
    try:
        upload = await loop.run_in_executor(executor, library.start_upload, folder, file_name)
    except LibraryError as error:
        return _library_error_response(error)

    try:
        async for chunk in request.stream():
            if chunk:
                await loop.run_in_executor(executor, upload.write, chunk)
        await loop.run_in_executor(executor, upload.finish)
    except LibraryError as error:
        await loop.run_in_executor(executor, upload.abort)
        return _library_error_response(error)
    except Exception:
        await loop.run_in_executor(executor, upload.abort)
        raise

    return JSONResponse(status_code=201, content={'path': upload.relative_path, 'size': upload.size})


async def _handle_library_folder_create(request: Request, library, executor):
    try:
        body = await _library_json_body(request)
    except LibraryError as error:
        return _library_error_response(error)

    loop = asyncio.get_running_loop()
    try:
        path = await loop.run_in_executor(executor, library.create_folder, body.get('parent'), body.get('name'))
    except LibraryError as error:
        return _library_error_response(error)
    return JSONResponse(status_code=201, content={'path': path})


async def _handle_library_entries_get(request: Request, library, executor):
    folder = request.query_params.get('folder')
    if folder is None:
        return JSONResponse(status_code=400, content={'error': {
            'code': 'invalid_request', 'message': "Missing query parameter 'folder'.",
        }})

    loop = asyncio.get_running_loop()
    try:
        entries = await loop.run_in_executor(executor, library.list_entries, folder)
    except LibraryError as error:
        return _library_error_response(error)
    return {'entries': entries}


async def _handle_library_entries_delete(request: Request, library, executor):
    try:
        body = await _library_json_body(request)
    except LibraryError as error:
        return _library_error_response(error)

    loop = asyncio.get_running_loop()
    try:
        deleted = await loop.run_in_executor(executor, library.delete_entries, body.get('paths'))
    except LibraryError as error:
        return _library_error_response(error)
    return {'deleted': deleted}


async def _handle_library_refresh(library, executor):
    loop = asyncio.get_running_loop()
    try:
        update_id = await loop.run_in_executor(executor, library.update)
    except LibraryError as error:
        return _library_error_response(error)
    return {'update_id': update_id}


def create_app(broker, executor, rpc_processor=process_request, library=None, library_executor=None,
                webapp_build_dir=None, logs_dir=None):
    if library is None:
        library = create_music_library()
    if library_executor is None:
        library_executor = executor

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

    @app.put('/api/v1/library/files')
    async def library_upload(request: Request):
        return await _handle_library_upload(request, library, library_executor)

    @app.post('/api/v1/library/folders')
    async def library_folder_create(request: Request):
        return await _handle_library_folder_create(request, library, library_executor)

    @app.get('/api/v1/library/entries')
    async def library_entries_get(request: Request):
        return await _handle_library_entries_get(request, library, library_executor)

    @app.delete('/api/v1/library/entries')
    async def library_entries_delete(request: Request):
        return await _handle_library_entries_delete(request, library, library_executor)

    @app.post('/api/v1/library/refresh')
    async def library_refresh():
        return await _handle_library_refresh(library, library_executor)

    # Registered last so it never shadows the /api/v1/* routes above: FastAPI/Starlette tries
    # routes in registration order, and this includes a catch-all.
    register_webapp_routes(
        app,
        build_dir=webapp_build_dir or default_webapp_build_dir(),
        logs_dir=logs_dir or default_logs_dir(),
    )

    return app


class FastApiServer(threading.Thread):
    """Run the browser API on an isolated asyncio event loop."""

    def __init__(self, bind_address=None, port=None, bus=None):
        super().__init__(name='FastApiServer', daemon=True)
        self.bind_address = bind_address or cfg.getn('api', 'bind_address', default='0.0.0.0')
        self.port = port if port is not None else cfg.getn('api', 'port', default=5556)
        self.bus = bus or jukebox.publishing.get_bus()
        self.broker = EventBroker(bus=self.bus)
        self._ready = threading.Event()
        self._startup_error = None
        self._loop = None
        self._server = None
        self._executor = None
        self._library_executor = None

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
        self._library_executor = ThreadPoolExecutor(
            max_workers=LIBRARY_EXECUTOR_WORKERS, thread_name_prefix='FastApiLibrary')
        app = create_app(self.broker, self._executor, library_executor=self._library_executor)

        config = uvicorn.Config(app, host=self.bind_address, port=self.port, loop='none', log_config=None)
        self._server = uvicorn.Server(config)

        # broker.publish is called synchronously from whatever thread published (see
        # jukebox.publishing.bus.EventBus); it hands off to this server's event loop itself via
        # asyncio.run_coroutine_threadsafe (see _WebSocketClient.write_message), so no separate
        # subscriber loop/bridging is needed here -- unlike the old ZMQ SUB-socket version.
        self.bus.register(self.broker.publish)

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
            self.bus.unregister(self.broker.publish)
            self._executor.shutdown(wait=False, cancel_futures=True)
            self._library_executor.shutdown(wait=False, cancel_futures=True)

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
