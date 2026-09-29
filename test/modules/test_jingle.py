import signal

import pytest

import jukebox.daemon
import jukebox.jingle
from jukebox.contract import OperationError
from jukebox.jingle import Jingle


@pytest.fixture
def played(monkeypatch):
    calls = []
    monkeypatch.setattr(jukebox.jingle, 'play_file', lambda path, volume, should_stop=None: calls.append((path, volume)))
    monkeypatch.setattr(jukebox.daemon, '_SHUTDOWN_SIGNAL', None)
    return calls


def test_startup_and_shutdown_sounds(start_modules, played, wait_for):
    manager, _ = start_modules([Jingle], {'jingle': {'startup_sound': 'start.wav', 'shutdown_sound': 'stop.wav',
                                                     'volume': 30}})
    assert wait_for(lambda: played == [('start.wav', 30)])
    manager.stop()
    assert played[-1] == ('stop.wav', 30)


def test_no_shutdown_sound_on_ctrl_c(start_modules, played, monkeypatch):
    manager, _ = start_modules([Jingle], {'jingle': {'shutdown_sound': 'stop.wav'}})
    monkeypatch.setattr(jukebox.daemon, '_SHUTDOWN_SIGNAL', signal.SIGINT)
    manager.stop()
    assert played == []


def test_play_action(start_modules, played, tmp_path, wait_for):
    sound = tmp_path / 'ding.wav'
    sound.write_bytes(b'')
    manager, _ = start_modules([Jingle], {})
    manager.catalog.call('jingle.play', {'sound': str(sound)})
    assert wait_for(lambda: played == [(str(sound), 100)])
    with pytest.raises(OperationError):
        manager.catalog.call('jingle.play', {'sound': str(tmp_path / 'missing.wav')})
