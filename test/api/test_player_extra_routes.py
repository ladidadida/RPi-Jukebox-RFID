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
    ctrl.get_player_type_and_version.return_value = 'jukebox-local-audio'
    ctrl.update.return_value = 7
    ctrl.update_wait.return_value = 7
    ctrl.get_current_song.return_value = {'file': 'a.mp3'}
    ctrl.playlistinfo.return_value = [{'file': 'a.mp3'}]
    ctrl.list_backends.return_value = ['local_audio', 'mpd']
    ctrl.get_active_backend.return_value = 'local_audio'
    ctrl.get_default_backend.return_value = 'local_audio'
    ctrl.select_backend.return_value = 'mpd'
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


def test_player_type(client, player_ctrl):
    response = client.get('/api/v1/player/type')
    assert response.status_code == 200
    assert response.json() == 'jukebox-local-audio'


def test_update(client, player_ctrl):
    response = client.post('/api/v1/player/update')
    assert response.status_code == 200
    assert response.json() == 7


def test_update_wait(client, player_ctrl):
    response = client.post('/api/v1/player/update-wait')
    assert response.status_code == 200
    player_ctrl.update_wait.assert_called_once_with()


def test_stop(client, player_ctrl):
    response = client.post('/api/v1/player/stop')
    assert response.status_code == 204
    player_ctrl.stop.assert_called_once_with()


def test_rewind(client, player_ctrl):
    response = client.post('/api/v1/player/rewind')
    assert response.status_code == 204
    player_ctrl.rewind.assert_called_once_with()


def test_replay(client, player_ctrl):
    response = client.post('/api/v1/player/replay')
    assert response.status_code == 204
    player_ctrl.replay.assert_called_once_with()


def test_replay_if_stopped(client, player_ctrl):
    response = client.post('/api/v1/player/replay-if-stopped')
    assert response.status_code == 204
    player_ctrl.replay_if_stopped.assert_called_once_with()


def test_resume(client, player_ctrl):
    response = client.post('/api/v1/player/resume')
    assert response.status_code == 204
    player_ctrl.resume.assert_called_once_with()


def test_current_song(client, player_ctrl):
    response = client.get('/api/v1/player/current-song', params={'param': 'x'})
    assert response.status_code == 200
    assert response.json() == {'file': 'a.mp3'}
    player_ctrl.get_current_song.assert_called_once_with('x')


def test_playlist(client, player_ctrl):
    response = client.get('/api/v1/player/playlist')
    assert response.status_code == 200
    assert response.json() == [{'file': 'a.mp3'}]


def test_flush_coverart_cache(client, player_ctrl):
    response = client.post('/api/v1/player/coverart/flush')
    assert response.status_code == 204
    player_ctrl.flush_coverart_cache.assert_called_once_with()


def test_list_backends(client, player_ctrl):
    response = client.get('/api/v1/player/backends')
    assert response.status_code == 200
    assert response.json() == ['local_audio', 'mpd']


def test_get_active_backend(client, player_ctrl):
    response = client.get('/api/v1/player/backends/active')
    assert response.status_code == 200
    assert response.json() == {'name': 'local_audio'}


def test_get_default_backend(client, player_ctrl):
    response = client.get('/api/v1/player/backends/default')
    assert response.status_code == 200
    assert response.json() == {'name': 'local_audio'}


def test_select_backend(client, player_ctrl):
    response = client.put('/api/v1/player/backends/active', json={'name': 'mpd'})
    assert response.status_code == 200
    assert response.json() == {'name': 'mpd'}
    player_ctrl.select_backend.assert_called_once_with('mpd')


def test_backend_specific_method_not_implemented_maps_to_501(client, player_ctrl):
    # e.g. local_audio doesn't implement resume/coverart -- PlayerCoordinator raises
    # NotImplementedError, not a raw 500.
    player_ctrl.resume.side_effect = NotImplementedError(
        "Player backend 'PlayerLocalAudio' does not support 'resume'")

    response = client.post('/api/v1/player/resume')

    assert response.status_code == 501


def test_queue_load(client, player_ctrl):
    response = client.post('/api/v1/player/queue', json={'folder': 'Stories'})
    assert response.status_code == 204
    player_ctrl.queue_load.assert_called_once_with('Stories')
