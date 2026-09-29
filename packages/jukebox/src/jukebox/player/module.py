"""The player core module: playback through registered backends, typed status events."""

import logging
import threading
from functools import partial
from typing import Any, Dict, List, Mapping, Optional

from pydantic import BaseModel

import jukebox.legacy_actions as legacy_actions
from jukebox.contract import CoreModule, action, event, extension_point, query
from jukebox.player.backend import PlayerBackend
from jukebox.player.coordinator import PlayerCoordinator
from jukebox.player.status import PlayerStatus, status_from_backend

logger = logging.getLogger('jb.player')

DEFAULT_BACKEND = 'local_audio'


class VolumeLevel(BaseModel):
    volume: int


class CoverArt(BaseModel):
    cover_url: Optional[str] = None


class BackendName(BaseModel):
    name: Optional[str] = None


class Player(CoreModule):
    """Playback of folders, songs and albums; backends plug in at ``player.backends``."""

    name = 'player'
    interface_version = '1.0'
    concurrency = 'threadsafe'

    status = event('status', PlayerStatus)
    backends = extension_point('backends', PlayerBackend)

    def __init__(self):
        self._ctx = None
        self._coordinator = PlayerCoordinator()
        self._configured_backend = DEFAULT_BACKEND

    # -- lifecycle ------------------------------------------------------------------------------

    def start(self, ctx) -> None:
        self._ctx = ctx
        self._configured_backend = ctx.config.setdefault('backend', value=DEFAULT_BACKEND)
        self.backends.on_register(self._add_backend)

        from jukebox.player.backends.local_audio import PlayerLocalAudio
        self.backends.register('local_audio', PlayerLocalAudio())
        if self._configured_backend == 'mpd':
            from jukebox.player.mpd_plugin import create_mpd_backend
            self.backends.register('mpd', create_mpd_backend())

    def _add_backend(self, name: str, backend: Any) -> None:
        backend.set_status_callback(partial(self._publish_status, name))
        is_configured = name == self._configured_backend
        self._coordinator.register_backend(name, backend, make_active=is_configured)
        if is_configured:
            self._coordinator.set_default_backend(name)

    def _publish_status(self, provider: str, raw: Mapping[str, Any]) -> None:
        self._ctx.publish(self.status, status_from_backend(raw, provider))

    def ready(self) -> None:
        if self._configured_backend not in self.backends:
            logger.error(f"Configured player backend '{self._configured_backend}' is not available "
                         f"(registered: {self.backends.names()}); is its plugin enabled?")
        self._configure_second_swipe()

    def _configure_second_swipe(self) -> None:
        entry = self._ctx.config.get('second_swipe_action', default=None)
        if not isinstance(entry, dict):
            return
        if 'action' not in entry and entry.get('alias', 'custom') != 'custom':
            return
        catalog = self._ctx.actions

        def param_names(action_id):
            return [p.name for p in catalog.operation(action_id).params] if action_id in catalog else None

        converted, problem = legacy_actions.convert(entry, param_names)
        if converted is None:
            logger.error(f"Ignoring player.second_swipe_action: {problem}")
            return
        try:
            catalog.validate(converted['action'], converted['args'])
        except Exception as error:
            logger.error(f"Ignoring player.second_swipe_action: {error}")
            return
        self._coordinator.set_second_swipe_action(
            lambda: catalog.call_ignore_errors(converted['action'], converted['args']))

    def stop(self) -> List[threading.Thread]:
        results = self._coordinator.exit()
        return [r for r in results if isinstance(r, threading.Thread)]

    # -- transport ------------------------------------------------------------------------------

    @action(path='/play')
    def play(self) -> None:
        """Start or resume playback."""
        self._coordinator.play()

    @action(path='/pause')
    def pause(self, state: int = 1) -> None:
        """Pause (state=1) or resume (state=0)."""
        self._coordinator.pause(state)

    @action(path='/toggle')
    def toggle(self) -> None:
        """Toggle between play and pause."""
        self._coordinator.toggle()

    @action(path='/next')
    def next(self) -> None:
        """Skip to the next song."""
        self._coordinator.next()

    @action(path='/prev')
    def prev(self) -> None:
        """Go back to the previous song."""
        self._coordinator.prev()

    @action(name='stop', path='/stop')
    def stop_playback(self) -> None:
        """Stop playback."""
        self._coordinator.stop()

    @action(path='/seek')
    def seek(self, position: float) -> None:
        """Jump to a position (seconds) in the current song."""
        self._coordinator.seek(position)

    @action(path='/shuffle')
    def shuffle(self, option: str = 'toggle') -> None:
        """Shuffle mode: 'toggle', 'enable' or 'disable'."""
        self._coordinator.shuffle(option)

    @action(path='/repeat')
    def repeat(self, option: str = 'toggle') -> None:
        """Repeat mode: 'toggle', 'enable', 'enable_repeat_single' or 'disable'."""
        self._coordinator.repeat(option)

    @action(path='/rewind')
    def rewind(self) -> None:
        """Restart the playlist from its first song."""
        self._coordinator.rewind()

    @action(path='/replay')
    def replay(self) -> None:
        """Replay the current folder from the start."""
        self._coordinator.replay()

    @action(path='/replay-if-stopped')
    def replay_if_stopped(self) -> None:
        """Replay the current folder if playback has stopped."""
        self._coordinator.replay_if_stopped()

    @action(path='/resume')
    def resume(self) -> None:
        """Resume the last played folder where it stopped."""
        self._coordinator.resume()

    # -- content --------------------------------------------------------------------------------

    @action(path='/folder')
    def play_folder(self, folder: str, recursive: bool = False) -> None:
        """Play a folder of the music library."""
        self._coordinator.play_folder(folder, recursive)

    @action()
    def play_card(self, folder: str, recursive: bool = False) -> None:
        """Play a folder; a second swipe of the same card runs the second-swipe action."""
        self._coordinator.play_card(folder, recursive)

    @action(path='/song')
    def play_single(self, song_url: str, provider: Optional[str] = None) -> None:
        """Play a single song."""
        self._coordinator.play_single(song_url, provider)

    @action(path='/album')
    def play_album(self, albumartist: str, album: str, content_uri: Optional[str] = None,
                   provider: Optional[str] = None) -> None:
        """Play an album."""
        self._coordinator.play_album(albumartist, album, content_uri, provider)

    @action(path='/queue')
    def queue_load(self, folder: str) -> None:
        """Load a folder into the queue without playing it."""
        self._coordinator.queue_load(folder)

    @action(path='/coverart/flush')
    def flush_coverart_cache(self) -> None:
        """Delete all cached cover art."""
        self._coordinator.flush_coverart_cache()

    @action(path='/update')
    def update(self) -> Any:
        """Rescan the music library of the default backend."""
        return self._coordinator.update()

    @action(path='/update-wait')
    def update_wait(self) -> Any:
        """Rescan the music library and wait for it to finish."""
        return self._coordinator.update_wait()

    # -- status and volume ----------------------------------------------------------------------

    @query(path='/status')
    def playerstatus(self) -> PlayerStatus:
        """Current player status."""
        name = self._coordinator.get_active_backend()
        return status_from_backend(self._coordinator.playerstatus(), name or '')

    @query(path='/volume')
    def get_volume(self) -> VolumeLevel:
        """Current playback volume of the active backend."""
        return VolumeLevel(volume=int(self._coordinator.get_volume()))

    @action(method='PUT', path='/volume')
    def set_volume(self, volume: int) -> VolumeLevel:
        """Set the playback volume of the active backend."""
        return VolumeLevel(volume=int(self._coordinator.set_volume(volume)))

    @query(path='/playlist')
    def playlistinfo(self) -> List[Dict[str, Any]]:
        """The current queue."""
        return self._coordinator.playlistinfo()

    @query(path='/current-song')
    def get_current_song(self, param: Optional[str] = None) -> Any:
        """Details of the current song."""
        return self._coordinator.get_current_song(param)

    @query(path='/type')
    def get_player_type_and_version(self) -> str:
        """Type and version of the active backend."""
        return self._coordinator.get_player_type_and_version()

    # -- library --------------------------------------------------------------------------------

    @query(path='/coverart/song')
    def get_single_coverart(self, song_url: str, provider: Optional[str] = None) -> CoverArt:
        """Cover art of a song."""
        return CoverArt(cover_url=self._coordinator.get_single_coverart(song_url, provider))

    @query(path='/coverart/album')
    def get_album_coverart(self, albumartist: str, album: str, content_uri: Optional[str] = None,
                           provider: Optional[str] = None) -> CoverArt:
        """Cover art of an album."""
        return CoverArt(cover_url=self._coordinator.get_album_coverart(albumartist, album, content_uri, provider))

    @query(path='/dirs')
    def list_all_dirs(self) -> List[Any]:
        """All files of the music library."""
        return self._coordinator.list_all_dirs()

    @query(path='/folder-content')
    def get_folder_content(self, folder: str) -> List[Any]:
        """Playable content of a folder."""
        return self._coordinator.get_folder_content(folder)

    @query(path='/albums')
    def list_albums(self, provider: Optional[str] = None) -> List[Any]:
        """All albums."""
        return self._coordinator.list_albums(provider)

    @query(path='/library/sources')
    def list_library_sources(self) -> List[Any]:
        """Library sources with their views."""
        return self._coordinator.list_library_sources()

    @query(path='/library/items')
    def list_library_items(self, provider: Optional[str] = None,
                           content_types: Optional[List[str]] = None) -> List[Any]:
        """Library items, optionally filtered by source and content type."""
        return self._coordinator.list_library_items(provider, content_types)

    @query(path='/songs')
    def list_songs_by_artist_and_album(self, albumartist: str, album: str, content_uri: Optional[str] = None,
                                       provider: Optional[str] = None) -> List[Any]:
        """Songs of an album."""
        return self._coordinator.list_songs_by_artist_and_album(albumartist, album, content_uri, provider)

    @query(path='/song-lookup')
    def get_song_by_url(self, song_url: str, provider: Optional[str] = None) -> Any:
        """Details of a song by its URL."""
        return self._coordinator.get_song_by_url(song_url, provider)

    # -- backends -------------------------------------------------------------------------------

    @query(path='/backends')
    def list_backends(self) -> List[str]:
        """Registered backends."""
        return self._coordinator.list_backends()

    @query(path='/backends/active')
    def get_active_backend(self) -> BackendName:
        """The backend playing right now."""
        return BackendName(name=self._coordinator.get_active_backend())

    @query(path='/backends/default')
    def get_default_backend(self) -> BackendName:
        """The backend used for content without an explicit provider."""
        return BackendName(name=self._coordinator.get_default_backend())

    @action(method='PUT', path='/backends/active')
    def select_backend(self, name: str) -> BackendName:
        """Stop the current backend and switch to another one."""
        return BackendName(name=self._coordinator.select_backend(name))
