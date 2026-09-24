from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

import jukebox.registry as registry
from jukebox.api.events import EventBroker
from jukebox.api.fastapi_server import create_app


@pytest.fixture
def misc_funcs():
    get_app_settings = Mock(return_value={'show_covers': True})
    set_app_settings = Mock()
    registry.register(get_app_settings, name='get_app_settings', package='misc')
    registry.register(set_app_settings, name='set_app_settings', package='misc')
    yield {'get_app_settings': get_app_settings, 'set_app_settings': set_app_settings}
    registry.unregister('misc')


@pytest.fixture
def cards_funcs():
    list_cards = Mock(return_value={'0001': {'func': 'player.ctrl.play_folder', 'description': ''}})
    register_card = Mock()
    delete_card = Mock()
    registry.register(list_cards, name='list_cards', package='cards')
    registry.register(register_card, name='register_card', package='cards')
    registry.register(delete_card, name='delete_card', package='cards')
    yield {'list_cards': list_cards, 'register_card': register_card, 'delete_card': delete_card}
    registry.unregister('cards')


@pytest.fixture
def client():
    executor = ThreadPoolExecutor(max_workers=1)
    app = create_app(EventBroker(), executor)
    with TestClient(app) as test_client:
        yield test_client
    executor.shutdown(wait=False, cancel_futures=True)


def test_get_settings(client, misc_funcs):
    response = client.get('/api/v1/settings')
    assert response.status_code == 200
    assert response.json() == {'show_covers': True}


def test_set_settings(client, misc_funcs):
    response = client.put('/api/v1/settings', json={'settings': {'show_covers': False}})
    assert response.status_code == 200
    misc_funcs['set_app_settings'].assert_called_once_with({'show_covers': False})


def test_list_cards(client, cards_funcs):
    response = client.get('/api/v1/cards')
    assert response.status_code == 200
    assert response.json() == {'0001': {'func': 'player.ctrl.play_folder', 'description': ''}}


def test_register_card(client, cards_funcs):
    response = client.post('/api/v1/cards', json={
        'card_id': '0002', 'cmd_alias': 'play', 'overwrite': True,
    })
    assert response.status_code == 201
    cards_funcs['register_card'].assert_called_once_with('0002', 'play', None, None, None, None, True)


def test_register_card_rejects_unknown_alias(client, cards_funcs):
    cards_funcs['register_card'].side_effect = KeyError("Unknown RPC command alias: 'bogus'")

    response = client.post('/api/v1/cards', json={'card_id': '0003', 'cmd_alias': 'bogus'})

    assert response.status_code == 400
    assert response.json()['error']['code'] == 'invalid_card_request'


def test_delete_card(client, cards_funcs):
    response = client.request('DELETE', '/api/v1/cards', json={'card_id': '0001'})
    assert response.status_code == 204
    cards_funcs['delete_card'].assert_called_once_with('0001')
