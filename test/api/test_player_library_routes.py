from unittest.mock import Mock

import pytest



@pytest.fixture
def player_ctrl():
    ctrl = Mock()
    ctrl.get_single_coverart.return_value = 'cover.jpg'
    ctrl.get_album_coverart.return_value = 'album.jpg'
    ctrl.list_all_dirs.return_value = [{'file': 'a.mp3'}]
    ctrl.get_folder_content.return_value = [{'type': 'file', 'name': 'a.mp3'}]
    ctrl.list_albums.return_value = [{'album': 'Stories'}]
    ctrl.list_library_sources.return_value = [{'id': 'local_audio', 'label': 'Local'}]
    ctrl.list_library_items.return_value = [{'album': 'Stories'}]
    ctrl.list_songs_by_artist_and_album.return_value = [{'file': 'a.mp3'}]
    ctrl.get_song_by_url.return_value = [{'file': 'a.mp3'}]
    return ctrl


@pytest.fixture
def client(player_ctrl, api_client, mocked_player):
    with api_client([mocked_player(player_ctrl)]) as test_client:
        yield test_client


def test_song_coverart(client, player_ctrl):
    response = client.get('/api/v1/player/coverart/song', params={'song_url': 'a.mp3'})
    assert response.status_code == 200
    assert response.json() == {'cover_url': 'cover.jpg'}
    player_ctrl.get_single_coverart.assert_called_once_with('a.mp3', None)


def test_album_coverart(client, player_ctrl):
    response = client.get('/api/v1/player/coverart/album', params={
        'albumartist': 'Reader', 'album': 'Stories',
    })
    assert response.status_code == 200
    assert response.json() == {'cover_url': 'album.jpg'}
    player_ctrl.get_album_coverart.assert_called_once_with('Reader', 'Stories', None, None)


def test_list_all_dirs(client, player_ctrl):
    response = client.get('/api/v1/player/dirs')
    assert response.status_code == 200
    assert response.json() == [{'file': 'a.mp3'}]


def test_folder_content(client, player_ctrl):
    response = client.get('/api/v1/player/folder-content', params={'folder': 'Stories'})
    assert response.status_code == 200
    player_ctrl.get_folder_content.assert_called_once_with('Stories')


def test_list_albums(client, player_ctrl):
    response = client.get('/api/v1/player/albums')
    assert response.status_code == 200
    assert response.json() == [{'album': 'Stories'}]


def test_library_sources(client, player_ctrl):
    response = client.get('/api/v1/player/library/sources')
    assert response.status_code == 200
    assert response.json() == [{'id': 'local_audio', 'label': 'Local'}]


def test_library_items_with_repeated_content_types(client, player_ctrl):
    response = client.get(
        '/api/v1/player/library/items',
        params=[('provider', 'local_audio'), ('content_types', 'album'), ('content_types', 'folder')])
    assert response.status_code == 200
    player_ctrl.list_library_items.assert_called_once_with('local_audio', ['album', 'folder'])


def test_library_items_without_content_types(client, player_ctrl):
    response = client.get('/api/v1/player/library/items')
    assert response.status_code == 200
    player_ctrl.list_library_items.assert_called_once_with(None, None)


def test_songs_by_artist_and_album(client, player_ctrl):
    response = client.get('/api/v1/player/songs', params={'albumartist': 'Reader', 'album': 'Stories'})
    assert response.status_code == 200
    assert response.json() == [{'file': 'a.mp3'}]
    player_ctrl.list_songs_by_artist_and_album.assert_called_once_with('Reader', 'Stories', None, None)


def test_song_lookup(client, player_ctrl):
    response = client.get('/api/v1/player/song-lookup', params={'song_url': 'a.mp3'})
    assert response.status_code == 200
    assert response.json() == [{'file': 'a.mp3'}]


def test_play_album(client, player_ctrl):
    response = client.post('/api/v1/player/album', json={'albumartist': 'Reader', 'album': 'Stories'})
    assert response.status_code == 204
    player_ctrl.play_album.assert_called_once_with('Reader', 'Stories', None, None)
