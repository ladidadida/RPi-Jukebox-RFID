import json
import socket
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
import zmq
from starlette.testclient import TestClient

from jukebox.api.fastapi_server import FastApiServer, create_app
from jukebox.api.server import EventBroker, MAX_MESSAGE_SIZE, PUBLISH_ENDPOINT
from jukebox.library import MusicLibrary


def _make_client(rpc_processor):
    executor = ThreadPoolExecutor(max_workers=1)
    app = create_app(EventBroker(), executor, rpc_processor)
    client = TestClient(app)
    return client, executor


@pytest.fixture
def library_client():
    executor = ThreadPoolExecutor(max_workers=1)
    library_directory = tempfile.TemporaryDirectory()
    library_updates = []
    library = MusicLibrary(
        lambda: library_directory.name,
        lambda: library_updates.append('update') or 'update-1',
    )
    app = create_app(EventBroker(), executor, lambda request: {'result': None}, library=library)
    client = TestClient(app)
    try:
        yield client, Path(library_directory.name), library_updates
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        library_directory.cleanup()


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


def test_http_rpc_rejects_oversized_body():
    client, executor = _make_client(lambda request: {'result': None})
    try:
        response = client.post(
            '/api/v1/rpc',
            headers={'Content-Type': 'application/json'},
            content=b' ' * (MAX_MESSAGE_SIZE + 1),
        )
        assert response.status_code == 413
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


def test_library_upload_create_delete_and_refresh(library_client):
    client, library_directory, library_updates = library_client

    folder_response = client.post(
        '/api/v1/library/folders',
        headers={'Content-Type': 'application/json'},
        content=json.dumps({'parent': '.', 'name': 'Album'}),
    )
    assert folder_response.status_code == 201
    assert folder_response.json() == {'path': 'Album'}

    upload_response = client.put(
        '/api/v1/library/files',
        params={'folder': 'Album', 'name': 'track.mp3'},
        headers={'Content-Type': 'audio/mpeg'},
        content=b'audio data',
    )
    assert upload_response.status_code == 201
    assert upload_response.json() == {'path': 'Album/track.mp3', 'size': 10}
    assert (library_directory / 'Album' / 'track.mp3').read_bytes() == b'audio data'

    list_response = client.get('/api/v1/library/entries', params={'folder': 'Album'})
    assert list_response.status_code == 200
    assert list_response.json() == {
        'entries': [{'name': 'track.mp3', 'relpath': 'Album/track.mp3', 'type': 'file'}],
    }

    duplicate_response = client.put(
        '/api/v1/library/files',
        params={'folder': 'Album', 'name': 'track.mp3'},
        content=b'replacement',
    )
    assert duplicate_response.status_code == 409
    assert duplicate_response.json()['error']['code'] == 'duplicate_name'

    refresh_response = client.post('/api/v1/library/refresh', content=b'')
    assert refresh_response.status_code == 200
    assert refresh_response.json() == {'update_id': 'update-1'}
    assert library_updates == ['update']

    delete_response = client.request(
        'DELETE',
        '/api/v1/library/entries',
        headers={'Content-Type': 'application/json'},
        content=json.dumps({'paths': ['Album']}),
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {'deleted': ['Album']}
    assert not (library_directory / 'Album').exists()


def test_library_endpoints_reject_invalid_types_and_paths(library_client):
    client, _library_directory, _library_updates = library_client

    unsupported = client.put(
        '/api/v1/library/files',
        params={'folder': '.', 'name': 'archive.zip'},
        content=b'archive',
    )
    assert unsupported.status_code == 415
    assert unsupported.json()['error']['code'] == 'unsupported_file_type'

    traversal = client.put(
        '/api/v1/library/files',
        params={'folder': '..', 'name': 'track.mp3'},
        content=b'audio',
    )
    assert traversal.status_code == 400
    assert traversal.json()['error']['code'] == 'invalid_path'

    delete_root = client.request(
        'DELETE',
        '/api/v1/library/entries',
        headers={'Content-Type': 'application/json'},
        content=json.dumps({'paths': ['.']}),
    )
    assert delete_root.status_code == 400
    assert delete_root.json()['error']['code'] == 'invalid_path'


def test_library_folder_create_rejects_oversized_body(library_client):
    client, _library_directory, _library_updates = library_client

    response = client.post(
        '/api/v1/library/folders',
        headers={'Content-Type': 'application/json'},
        content=b' ' * (MAX_MESSAGE_SIZE + 1),
    )
    assert response.status_code == 413
    assert response.json()['error']['code'] == 'request_too_large'


def test_blocking_rpc_does_not_block_health():
    started = threading.Event()
    release = threading.Event()

    def blocking_processor(request):
        started.set()
        release.wait(1)
        return {'result': 'done', 'id': request.get('id')}

    executor = ThreadPoolExecutor(max_workers=4)
    app = create_app(EventBroker(), executor, blocking_processor)
    client = TestClient(app)
    try:
        results = {}

        def do_rpc():
            response = client.post(
                '/api/v1/rpc',
                headers={'Content-Type': 'application/json'},
                content=json.dumps({'id': 'request'}),
            )
            results['rpc'] = response

        rpc_thread = threading.Thread(target=do_rpc)
        rpc_thread.start()
        assert started.wait(1)

        health = client.get('/api/v1/health')
        assert health.status_code == 200

        release.set()
        rpc_thread.join(1)
        assert results['rpc'].json()['result'] == 'done'
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
