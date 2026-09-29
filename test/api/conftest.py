from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

import pytest
from starlette.testclient import TestClient

from jukebox.api.events import EventBroker
from jukebox.api.fastapi_server import create_app
from jukebox.cfghandler import ConfigHandler
from jukebox.contract.manager import ModuleManager
from jukebox.player.module import Player
from jukebox.publishing.bus import EventBus


def _mocked_player(ctrl):
    """A player module whose coordinator is ``ctrl`` (no real backends)."""
    class MockedPlayer(Player):
        def start(self, ctx):
            self._ctx = ctx
            self._coordinator = ctrl

    return MockedPlayer


@contextmanager
def _api_client(core_modules, config=None):
    cfg = ConfigHandler('test')
    cfg.config_dict(config or {})
    manager = ModuleManager(core_modules, cfg, EventBus(), plugins={}, strict=True)
    manager.load()
    manager.start()
    manager.ready()
    executor = ThreadPoolExecutor(max_workers=1)
    app = create_app(EventBroker(), executor, modules=manager)
    try:
        with TestClient(app) as client:
            client.modules = manager
            yield client
    finally:
        manager.stop()
        executor.shutdown(wait=False, cancel_futures=True)


@pytest.fixture
def mocked_player():
    return _mocked_player


@pytest.fixture
def api_client():
    return _api_client
