# -*- coding: utf-8 -*-
"""
Default player backend: decodes audio directly (PyAV) and writes PCM to the machine's normal
audio output (sounddevice/PortAudio) -- no mpd, no external player process, works on any Linux
box. See documentation/developers/roadmap-core-architecture.md, "Advanced plugin system".

Folder scanning reuses `jukebox.playlistgenerator.PlaylistCollector` (already backend-agnostic --
`backends/mpd.py` uses the exact same class, just pushes the resulting paths into MPD's queue
instead of this backend's own in-process one).

Playback runs on one dedicated worker thread. Every control method (play/pause/stop/next/prev/
seek/play_folder/...) updates `_state`/`_index`/`_position` under `_cv` and sets `_abort` to
interrupt whatever the worker is currently doing; the worker reopens/seeks the current track
whenever it's told to (re)start one. This keeps the state machine in one place instead of trying
to signal a live decode loop with finer-grained commands.
"""
import array
import functools
import logging
import os
import random
import threading

import av
from av.audio.resampler import AudioResampler
import sounddevice as sd

import jukebox.player
import jukebox.cfghandler
import jukebox.registry as plugs
import jukebox.utils as utils
import jukebox.multitimer as multitimer
import jukebox.publishing as publishing
import jukebox.playlistgenerator as playlistgenerator

from jukebox.nv_manager import nv_manager
from jukebox.player.coordinator import PlayerCoordinator

logger = logging.getLogger('jb.PlayerLocalAudio')
cfg = jukebox.cfghandler.get_handler('jukebox')

SAMPLE_RATE = 44100
CHANNELS = 2


def _scale_volume(data: bytes, volume: int) -> bytes:
    """Scale packed s16 PCM by volume (0-100). No-op at full volume (the common case)."""
    if volume >= 100:
        return data
    factor = max(0, volume) / 100.0
    samples = array.array('h')
    samples.frombytes(data)
    for i, s in enumerate(samples):
        samples[i] = int(s * factor)
    return samples.tobytes()


class AudioSink:
    """What a decoded track is written to. Exists so tests don't need a real audio device."""

    def open(self, samplerate: int, channels: int) -> None:
        raise NotImplementedError

    def write(self, data: bytes) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


class PortAudioSink(AudioSink):
    """Real output via sounddevice/PortAudio. Falls back to silent (no-op) if no device is
    available -- e.g. the no-audio docker dev stack, or a CI box -- rather than raising and
    killing the daemon."""

    def __init__(self):
        self._stream = None

    def open(self, samplerate, channels):
        try:
            self._stream = sd.RawOutputStream(samplerate=samplerate, channels=channels, dtype='int16')
            self._stream.start()
        except Exception as e:
            logger.warning(f"No audio output device available ({e.__class__.__name__}: {e}); playing silently")
            self._stream = None

    def write(self, data):
        if self._stream is None:
            return
        try:
            self._stream.write(data)
        except Exception as e:
            logger.warning(f"Audio output error, playing silently for the rest of this track: {e}")
            self._stream = None

    def close(self):
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None


class PlayerLocalAudio:
    """Decode-and-output player backend. See module docstring for the state machine."""

    def __init__(self):
        self.nvm = nv_manager()
        self._status_store = self.nvm.load(
            cfg.setndefault('player', 'status_file', value='shared/settings/local_audio_status.json')
        )
        if not self._status_store:
            self._status_store['last_played_folder'] = ''

        self._cv = threading.Condition(threading.RLock())
        self._abort = threading.Event()
        self._closing = False
        self._active = False

        self._queue: list[str] = []
        self._index = -1
        self._position = 0.0
        self._state = 'stop'           # 'play' | 'pause' | 'stop'
        self._random = False
        self._repeat_mode = 'off'      # 'off' | 'repeat' | 'single'
        self._volume = int(cfg.setndefault('player', 'volume', value=80))
        self._last_played_folder = self._status_store.get('last_played_folder', '')

        self._second_swipe_action_dict = {
            'toggle': self.toggle,
            'play': self.play,
            'skip': self.next,
            'rewind': self.rewind,
            'replay': self.replay,
            'replay_if_stopped': self.replay_if_stopped,
        }
        self.second_swipe_action = None
        self._decode_2nd_swipe_option()

        self._end_of_playlist_next_action = utils.get_config_action(
            cfg, 'player', 'end_of_playlist_next_action', 'none',
            {'rewind': self.rewind, 'stop': self.stop, 'none': lambda: None}, logger)
        self._stopped_prev_action = utils.get_config_action(
            cfg, 'player', 'stopped_prev_action', 'prev',
            {'rewind': self.rewind, 'prev': self._prev_in_stopped_state, 'none': lambda: None}, logger)
        self._stopped_next_action = utils.get_config_action(
            cfg, 'player', 'stopped_next_action', 'next',
            {'rewind': self.rewind, 'next': self._next_in_stopped_state, 'none': lambda: None}, logger)

        self._sink = PortAudioSink()
        self._worker = threading.Thread(target=self._run, name='LocalAudioPlayback', daemon=True)
        self._worker.start()

        self._status_thread = multitimer.GenericEndlessTimerClass(
            'local_audio.timer_status', 0.25, self._publish_status)
        self._status_thread.start()

    # -- worker -----------------------------------------------------------------------------

    def _run(self):
        while True:
            with self._cv:
                while self._state != 'play' and not self._closing:
                    self._cv.wait()
                if self._closing:
                    return
                index = self._index
                position = self._position
            if not (0 <= index < len(self._queue)):
                with self._cv:
                    self._state = 'stop'
                continue
            self._abort.clear()
            ended_naturally = self._decode_track(self._queue[index], position)
            with self._cv:
                if self._closing:
                    return
                if not ended_naturally or self._state != 'play' or self._index != index:
                    # Interrupted by an external control call (stop/pause/next/prev/seek/new
                    # play_folder) -- it already set _index/_position/_state to what it wants.
                    continue
                if self._repeat_mode == 'single':
                    self._position = 0.0
                elif self._random and len(self._queue) > 1:
                    self._index = random.randrange(len(self._queue))
                    self._position = 0.0
                elif index + 1 < len(self._queue):
                    self._index = index + 1
                    self._position = 0.0
                elif self._repeat_mode == 'repeat':
                    self._index = 0
                    self._position = 0.0
                else:
                    self._state = 'stop'
                    self._position = 0.0
                    self._end_of_playlist_next_action()

    def _decode_track(self, path: str, start_position: float) -> bool:
        """Decode+play `path` from `start_position`. Returns True if it ran to completion (or
        failed to decode at all -- either way, the caller should move on), False if `_abort`
        interrupted it early."""
        logger.info(f"Playing '{path}' from {start_position:.3f}s")
        try:
            container = av.open(path)
        except Exception as e:
            logger.error(f"Could not open '{path}': {e.__class__.__name__}: {e}")
            return True
        try:
            try:
                return self._decode_loop(container, start_position)
            except Exception as e:
                # A single bad/corrupt file must not take down the whole playback worker --
                # treat it as "ended" so the queue moves on to the next track.
                logger.error(f"Error decoding '{path}', skipping: {e.__class__.__name__}: {e}")
                return True
        finally:
            container.close()

    def _decode_loop(self, container, start_position: float) -> bool:
        stream = container.streams.audio[0]
        resampler = AudioResampler(format='s16', layout='stereo', rate=SAMPLE_RATE)
        if start_position:
            try:
                container.seek(int(start_position * 1_000_000), backward=True)
            except Exception as e:
                logger.warning(f"Seek to {start_position:.3f}s failed, starting from the top: {e}")
        self._sink.open(SAMPLE_RATE, CHANNELS)
        try:
            for frame in container.decode(stream):
                if self._abort.is_set():
                    return False
                for rframe in resampler.resample(frame):
                    if self._abort.is_set():
                        return False
                    n = rframe.samples * CHANNELS * 2
                    data = bytes(rframe.planes[0])[:n]
                    self._sink.write(_scale_volume(data, self._volume))
                    self._position += rframe.samples / SAMPLE_RATE
            return True
        finally:
            self._sink.close()

    def _jump_to(self, index: int, position: float = 0.0):
        with self._cv:
            self._index = index
            self._position = position
            self._state = 'play'
            self._abort.set()
            self._cv.notify_all()

    def _prev_in_stopped_state(self):
        self._jump_to(max(0, self._index - 1))

    def _next_in_stopped_state(self):
        pos = self._index + 1
        if pos > len(self._queue) - 1:
            return self._end_of_playlist_next_action()
        self._jump_to(pos)

    # -- second-swipe / config ---------------------------------------------------------------

    def _decode_2nd_swipe_option(self):
        action = cfg.setndefault('player', 'second_swipe_action', 'alias', value='none').lower()
        if action not in [*self._second_swipe_action_dict, 'none', 'custom']:
            logger.error(f"Config player.second_swipe_action must be one of "
                         f"{[*self._second_swipe_action_dict, 'none', 'custom']}. Ignore setting.")
        if action in self._second_swipe_action_dict:
            self.second_swipe_action = self._second_swipe_action_dict[action]
        if action == 'custom':
            custom_action = utils.decode_rpc_call(cfg.getn('player', 'second_swipe_action', default=None))
            self.second_swipe_action = functools.partial(plugs.call_ignore_errors,
                                                          custom_action['package'],
                                                          custom_action['plugin'],
                                                          custom_action['method'],
                                                          custom_action['args'],
                                                          custom_action['kwargs'])

    # -- coordinator-facing surface -----------------------------------------------------------

    def set_active(self, active):
        self._active = active
        if active:
            publishing.get_publisher().send('playerstatus', self._status_dict())

    def _publish_status(self):
        if self._active:
            publishing.get_publisher().send('playerstatus', self._status_dict())

    def _status_dict(self):
        with self._cv:
            index, position, state, queue_len = self._index, self._position, self._state, len(self._queue)
            current_file = self._queue[index] if 0 <= index < queue_len else None
        return {
            'state': state,
            'song': str(index),
            'pos': str(index),
            'file': current_file,
            'elapsed': f'{position:.3f}',
            'playlistlength': str(queue_len),
            'volume': str(self._volume),
            'random': '1' if self._random else '0',
            'repeat': '1' if self._repeat_mode in ('repeat', 'single') else '0',
            'single': '1' if self._repeat_mode == 'single' else '0',
            'provider': 'local_audio',
        }

    @plugs.tag
    def get_player_type_and_version(self):
        return f"jukebox-local-audio (pyav {av.__version__}, sounddevice {sd.__version__})"

    @plugs.tag
    def play(self):
        with self._cv:
            if not self._queue:
                logger.warning("play() called with nothing queued")
                return
            self._state = 'play'
            self._cv.notify_all()

    @plugs.tag
    def stop(self):
        with self._cv:
            self._state = 'stop'
            self._position = 0.0
            self._abort.set()

    @plugs.tag
    def pause(self, state: int = 1):
        with self._cv:
            if state:
                self._state = 'pause'
                self._abort.set()
            else:
                self._state = 'play'
                self._cv.notify_all()

    @plugs.tag
    def prev(self):
        with self._cv:
            if self._state == 'stop':
                return self._stopped_prev_action()
            new_index = max(0, self._index - 1)
        self._jump_to(new_index)

    @plugs.tag
    def next(self):
        with self._cv:
            if self._state == 'stop':
                return self._stopped_next_action()
            if self._index >= len(self._queue) - 1:
                return self._end_of_playlist_next_action()
            new_index = self._index + 1
        self._jump_to(new_index)

    @plugs.tag
    def seek(self, new_time):
        with self._cv:
            self._position = float(new_time)
            self._abort.set()

    @plugs.tag
    def rewind(self):
        """Re-start current playlist from the first track."""
        self._jump_to(0)

    @plugs.tag
    def replay(self):
        """Re-start playing the last-played folder."""
        self.play_folder(self._last_played_folder)

    @plugs.tag
    def toggle(self):
        with self._cv:
            if self._state == 'play':
                return self.pause(1)
            return self.pause(0)

    @plugs.tag
    def replay_if_stopped(self):
        with self._cv:
            if self._state == 'stop':
                self.replay()

    @plugs.tag
    def shuffle(self, option='toggle'):
        with self._cv:
            if option == 'toggle':
                self._random = not self._random
            elif option == 'enable':
                self._random = True
            elif option == 'disable':
                self._random = False
            else:
                logger.error(f"'{option}' does not exist for 'shuffle'")

    @plugs.tag
    def repeat(self, option='toggle'):
        with self._cv:
            if option == 'toggle':
                self._repeat_mode = {'off': 'repeat', 'repeat': 'single', 'single': 'off'}[self._repeat_mode]
            elif option == 'toggle_repeat':
                self._repeat_mode = 'off' if self._repeat_mode == 'repeat' else 'repeat'
            elif option == 'toggle_repeat_single':
                self._repeat_mode = 'off' if self._repeat_mode == 'single' else 'single'
            elif option == 'enable_repeat':
                self._repeat_mode = 'repeat'
            elif option == 'enable_repeat_single':
                self._repeat_mode = 'single'
            elif option == 'disable':
                self._repeat_mode = 'off'
            else:
                logger.error(f"'{option}' does not exist for 'repeat'")

    @plugs.tag
    def get_current_song(self, param):
        return self._status_dict()

    @plugs.tag
    def map_filename_to_playlist_pos(self, filename):
        raise NotImplementedError

    @plugs.tag
    def remove(self):
        raise NotImplementedError

    @plugs.tag
    def move(self):
        raise NotImplementedError

    @plugs.tag
    def play_single(self, song_url):
        with self._cv:
            self._queue = [song_url]
            self._index = 0
            self._position = 0.0
            self._state = 'play'
            self._abort.set()
            self._cv.notify_all()

    def is_second_swipe(self, folder: str) -> bool:
        return self.second_swipe_action is not None and self._last_played_folder == folder

    def play_second_swipe(self):
        self.second_swipe_action()

    @plugs.tag
    def get_folder_content(self, folder: str):
        plc = playlistgenerator.PlaylistCollector(jukebox.player.get_music_library_path())
        plc.get_directory_content(folder)
        return plc.playlist

    @plugs.tag
    def play_folder(self, folder: str, recursive: bool = False) -> None:
        plc = playlistgenerator.PlaylistCollector(jukebox.player.get_music_library_path())
        plc.parse(folder, recursive)
        paths = list(plc)
        with self._cv:
            self._queue = paths
            self._last_played_folder = folder
            self._status_store['last_played_folder'] = folder
            if paths:
                self._index = 0
                self._position = 0.0
                self._state = 'play'
                self._abort.set()
                self._cv.notify_all()
            else:
                logger.warning(f"Folder '{folder}' has no playable content")
                self._index = -1
                self._state = 'stop'
        self._status_store.save_to_json()

    @plugs.tag
    def queue_load(self, folder):
        pass

    @plugs.tag
    def playerstatus(self):
        return self._status_dict()

    @plugs.tag
    def playlistinfo(self):
        with self._cv:
            return [{'file': path, 'pos': str(i)} for i, path in enumerate(self._queue)]

    @plugs.tag
    def list_all_dirs(self):
        base = os.path.expanduser(jukebox.player.get_music_library_path())
        result = []
        for root, _dirs, files in os.walk(base):
            for f in files:
                result.append({'file': os.path.relpath(os.path.join(root, f), base)})
        return result

    def get_volume(self):
        return self._volume

    def set_volume(self, volume):
        with self._cv:
            self._volume = max(0, min(100, int(volume)))
        return self._volume

    def exit(self):
        logger.debug("Exit routine of PlayerLocalAudio started")
        self._status_thread.close()
        with self._cv:
            self._closing = True
            self._abort.set()
            self._cv.notify_all()
        self._status_store.save_to_json()
        return self._worker


def initialize():
    """Create the coordinator with local_audio as its sole backend and register it as 'player.ctrl'."""
    player_ctrl = PlayerCoordinator(jukebox.player.play_card_callbacks)
    player_ctrl.register_backend('local_audio', PlayerLocalAudio())
    plugs.register(player_ctrl, name='ctrl', package='player')
    return player_ctrl
