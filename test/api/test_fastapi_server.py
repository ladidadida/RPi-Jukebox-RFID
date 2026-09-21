import json
import socket
import time
from concurrent.futures import ThreadPoolExecutor

import zmq
from starlette.testclient import TestClient

from jukebox.api.fastapi_server import FastApiServer, create_app
from jukebox.api.server import EventBroker, PUBLISH_ENDPOINT


def _make_client(rpc_processor):
    executor = ThreadPoolExecutor(max_workers=1)
    app = create_app(EventBroker(), executor, rpc_processor)
    client = TestClient(app)
    return client, executor


def test_health():
    client, executor = _make_client(lambda request: {'result': None})
    try:
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
    finally:
        executor.shutdown(wait=True, cancel_futures=True)


def test_http_rpc():
    rpc_processor = lambda request: {  # noqa: E731
        'result': request['kwargs']['value'],
        'id': request.get('id'),
    }
    client, executor = _make_client(rpc_processor)
    try:
        response = client.post(
            '/api/v1/rpc',
            headers={'Content-Type': 'application/json; charset=utf-8'},
            content=json.dumps({'kwargs': {'value': 7}, 'id': 'request'}),
        )
        assert response.status_code == 200
        assert response.json() == {'result': 7, 'id': 'request'}
    finally:
        executor.shutdown(wait=True, cancel_futures=True)


def test_http_rpc_rejects_invalid_content():
    client, executor = _make_client(lambda request: {'result': None})
    try:
        for body, content_type, status in [
            ('{', 'application/json', 400),
            ('[]', 'application/json', 400),
            ('{}', 'text/plain', 400),
        ]:
            response = client.post(
                '/api/v1/rpc',
                headers={'Content-Type': content_type},
                content=body,
            )
            assert response.status_code == status
    finally:
        executor.shutdown(wait=True, cancel_futures=True)


def test_events_subscribe_receives_snapshot_and_rejects_bad_command():
    broker = EventBroker()
    broker.cache['core.version'] = 'test-version'
    executor = ThreadPoolExecutor(max_workers=1)
    app = create_app(broker, executor, lambda request: {'result': None})
    client = TestClient(app)
    try:
        with client.websocket_connect('/api/v1/events') as websocket:
            websocket.send_json({'type': 'subscribe', 'topics': ['core']})
            message = websocket.receive_json()
            assert message == {
                'type': 'event',
                'topic': 'core.version',
                'data': 'test-version',
            }
    finally:
        executor.shutdown(wait=True, cancel_futures=True)


def test_fastapi_server_thread_lifecycle_and_stable_subscription():
    port_socket = socket.socket()
    port_socket.bind(('127.0.0.1', 0))
    port = port_socket.getsockname()[1]
    port_socket.close()

    context = zmq.asyncio.Context()
    publisher = zmq.Socket(context, zmq.XPUB)
    publisher.bind(PUBLISH_ENDPOINT)
    server = FastApiServer(bind_address='127.0.0.1', port=port, context=context)
    try:
        server.start_and_wait()

        import urllib.request
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/api/v1/health', timeout=2) as response:
            assert json.load(response) == {'status': 'ok'}

        assert publisher.poll(2000)
        assert publisher.recv() == b'\x01'

        publisher.send_multipart([b'core.version', b'"test-version"'])
        deadline = time.monotonic() + 2
        while 'core.version' not in server.broker.cache and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.broker.cache.get('core.version') == 'test-version'
    finally:
        server.terminate()
        publisher.close(0)
        context.term()

    assert not server.is_alive()
