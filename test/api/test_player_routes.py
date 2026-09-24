from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

import jukebox.registry as registry
from jukebox.api.events import EventBroker
from jukebox.api.fastapi_server import create_app


@pytest.fixture
def player_ctrl():
    ctrl = Mock()
    ctrl.get_volume.return_value = 42
    ctrl.set_volume.return_value = 55
    ctrl.playerstatus.return_value = {'state': 'play', 'volume': '42'}
    registry.register(ctrl, name='ctrl', package='player')
    yield ctrl
    registry.unregister('player', 'ctrl')


@pytest.fixture
def client():
    executor = ThreadPoolExecutor(max_workers=1)
    app = create_app(EventBroker(), executor)
    with TestClient(app) as test_client:
        yield test_client
    executor.shutdown(wait=False, cancel_futures=True)


def test_play(client, player_ctrl):
    response = client.post('/api/v1/player/play')
    assert response.status_code == 204
    player_ctrl.play.assert_called_once_with()


def test_pause_defaults_to_state_1(client, player_ctrl):
    response = client.post('/api/v1/player/pause', json={})
    assert response.status_code == 204
    player_ctrl.pause.assert_called_once_with(1)


def test_pause_with_explicit_state(client, player_ctrl):
    response = client.post('/api/v1/player/pause', json={'state': 0})
    assert response.status_code == 204
    player_ctrl.pause.assert_called_once_with(0)


def test_toggle(client, player_ctrl):
    response = client.post('/api/v1/player/toggle')
    assert response.status_code == 204
    player_ctrl.toggle.assert_called_once_with()


def test_next(client, player_ctrl):
    response = client.post('/api/v1/player/next')
    assert response.status_code == 204
    player_ctrl.next.assert_called_once_with()


def test_prev(client, player_ctrl):
    response = client.post('/api/v1/player/prev')
    assert response.status_code == 204
    player_ctrl.prev.assert_called_once_with()


def test_seek(client, player_ctrl):
    response = client.post('/api/v1/player/seek', json={'position': 12.5})
    assert response.status_code == 204
    player_ctrl.seek.assert_called_once_with(12.5)


def test_seek_requires_position(client, player_ctrl):
    response = client.post('/api/v1/player/seek', json={})
    assert response.status_code == 422
    player_ctrl.seek.assert_not_called()


def test_shuffle_defaults_to_toggle(client, player_ctrl):
    response = client.post('/api/v1/player/shuffle', json={})
    assert response.status_code == 204
    player_ctrl.shuffle.assert_called_once_with('toggle')


def test_repeat_with_explicit_option(client, player_ctrl):
    response = client.post('/api/v1/player/repeat', json={'option': 'enable_repeat'})
    assert response.status_code == 204
    player_ctrl.repeat.assert_called_once_with('enable_repeat')


def test_play_folder(client, player_ctrl):
    response = client.post('/api/v1/player/folder', json={'folder': 'Stories', 'recursive': True})
    assert response.status_code == 204
    player_ctrl.play_folder.assert_called_once_with('Stories', True)


def test_play_folder_recursive_defaults_to_false(client, player_ctrl):
    response = client.post('/api/v1/player/folder', json={'folder': 'Stories'})
    assert response.status_code == 204
    player_ctrl.play_folder.assert_called_once_with('Stories', False)


def test_play_song(client, player_ctrl):
    response = client.post('/api/v1/player/song', json={'song_url': 'Stories/01.mp3'})
    assert response.status_code == 204
    player_ctrl.play_single.assert_called_once_with('Stories/01.mp3')


def test_get_status(client, player_ctrl):
    response = client.get('/api/v1/player/status')
    assert response.status_code == 200
    assert response.json() == {'state': 'play', 'volume': '42'}


def test_get_volume(client, player_ctrl):
    response = client.get('/api/v1/player/volume')
    assert response.status_code == 200
    assert response.json() == {'volume': 42}


def test_set_volume(client, player_ctrl):
    response = client.put('/api/v1/player/volume', json={'volume': 55})
    assert response.status_code == 200
    assert response.json() == {'volume': 55}
    player_ctrl.set_volume.assert_called_once_with(55)


def test_player_routes_appear_in_openapi_schema(client):
    schema = client.get('/openapi.json').json()
    assert '/api/v1/player/play' in schema['paths']
    assert '/api/v1/player/volume' in schema['paths']
