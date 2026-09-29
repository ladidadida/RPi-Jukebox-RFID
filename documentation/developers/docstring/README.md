# None

## Table of Contents

* [jukebox](#jukebox)
* [jukebox.utils](#jukebox.utils)
  * [get\_config\_action](#jukebox.utils.get_config_action)
  * [get\_git\_state](#jukebox.utils.get_git_state)
* [jukebox.jingle](#jukebox.jingle)
  * [Jingle](#jukebox.jingle.Jingle)
    * [play](#jukebox.jingle.Jingle.play)
* [jukebox.library.index](#jukebox.library.index)
  * [read\_tags](#jukebox.library.index.read_tags)
  * [LibraryIndex](#jukebox.library.index.LibraryIndex)
    * [relative](#jukebox.library.index.LibraryIndex.relative)
    * [scan](#jukebox.library.index.LibraryIndex.scan)
    * [albums](#jukebox.library.index.LibraryIndex.albums)
* [jukebox.library.files](#jukebox.library.files)
  * [LibraryError](#jukebox.library.files.LibraryError)
  * [resolve\_library\_path](#jukebox.library.files.resolve_library_path)
  * [UploadSession](#jukebox.library.files.UploadSession)
  * [MusicLibrary](#jukebox.library.files.MusicLibrary)
* [jukebox.library.module](#jukebox.library.module)
  * [LibrarySource](#jukebox.library.module.LibrarySource)
    * [describe](#jukebox.library.module.LibrarySource.describe)
    * [list\_items](#jukebox.library.module.LibrarySource.list_items)
    * [cover](#jukebox.library.module.LibrarySource.cover)
  * [song\_from\_source](#jukebox.library.module.song_from_source)
  * [Library](#jukebox.library.module.Library)
    * [list\_entries](#jukebox.library.module.Library.list_entries)
    * [create\_folder](#jukebox.library.module.Library.create_folder)
    * [delete\_entries](#jukebox.library.module.Library.delete_entries)
    * [refresh](#jukebox.library.module.Library.refresh)
    * [list\_sources](#jukebox.library.module.Library.list_sources)
    * [list\_items](#jukebox.library.module.Library.list_items)
    * [list\_songs](#jukebox.library.module.Library.list_songs)
    * [get\_song](#jukebox.library.module.Library.get_song)
    * [search](#jukebox.library.module.Library.search)
    * [get\_song\_cover](#jukebox.library.module.Library.get_song_cover)
    * [get\_album\_cover](#jukebox.library.module.Library.get_album_cover)
    * [flush\_covers](#jukebox.library.module.Library.flush_covers)
* [jukebox.library.covers](#jukebox.library.covers)
  * [CoverCache](#jukebox.library.covers.CoverCache)
    * [cover\_for](#jukebox.library.covers.CoverCache.cover_for)
* [jukebox.library](#jukebox.library)
* [jukebox.rfid.reader](#jukebox.rfid.reader)
  * [ReaderDriver](#jukebox.rfid.reader.ReaderDriver)
    * [create\_reader](#jukebox.rfid.reader.ReaderDriver.create_reader)
  * [CardRemovalTimer](#jukebox.rfid.reader.CardRemovalTimer)
  * [Rfid](#jukebox.rfid.reader.Rfid)
    * [resolve\_config\_action](#jukebox.rfid.reader.Rfid.resolve_config_action)
    * [list\_readers](#jukebox.rfid.reader.Rfid.list_readers)
* [jukebox.rfid.readerbase](#jukebox.rfid.readerbase)
  * [ReaderBaseClass](#jukebox.rfid.readerbase.ReaderBaseClass)
* [jukebox.rfid](#jukebox.rfid)
* [jukebox.rfid.cards](#jukebox.rfid.cards)
  * [Cards](#jukebox.rfid.cards.Cards)
    * [list\_cards](#jukebox.rfid.cards.Cards.list_cards)
    * [get\_card](#jukebox.rfid.cards.Cards.get_card)
    * [register\_card](#jukebox.rfid.cards.Cards.register_card)
    * [delete\_card](#jukebox.rfid.cards.Cards.delete_card)
* [jukebox.rfid.cardutils](#jukebox.rfid.cardutils)
  * [card\_command\_to\_str](#jukebox.rfid.cardutils.card_command_to_str)
* [jukebox.volume](#jukebox.volume)
  * [PlayerMixer](#jukebox.volume.PlayerMixer)
  * [PulseMixer](#jukebox.volume.PulseMixer)
  * [Volume](#jukebox.volume.Volume)
    * [get\_volume](#jukebox.volume.Volume.get_volume)
    * [set\_volume](#jukebox.volume.Volume.set_volume)
    * [change\_volume](#jukebox.volume.Volume.change_volume)
    * [mute](#jukebox.volume.Volume.mute)
    * [set\_soft\_max\_volume](#jukebox.volume.Volume.set_soft_max_volume)
    * [get\_outputs](#jukebox.volume.Volume.get_outputs)
    * [set\_output](#jukebox.volume.Volume.set_output)
    * [toggle\_output](#jukebox.volume.Volume.toggle_output)
    * [fade\_out](#jukebox.volume.Volume.fade_out)
* [jukebox.nv\_manager](#jukebox.nv_manager)
* [jukebox.publishing.bus](#jukebox.publishing.bus)
  * [EventBus](#jukebox.publishing.bus.EventBus)
    * [publish](#jukebox.publishing.bus.EventBus.publish)
    * [resend](#jukebox.publishing.bus.EventBus.resend)
    * [cache\_snapshot](#jukebox.publishing.bus.EventBus.cache_snapshot)
* [jukebox.publishing](#jukebox.publishing)
  * [get\_bus](#jukebox.publishing.get_bus)
* [jukebox.playlistgenerator](#jukebox.playlistgenerator)
  * [TYPE\_DECODE](#jukebox.playlistgenerator.TYPE_DECODE)
  * [PlaylistCollector](#jukebox.playlistgenerator.PlaylistCollector)
    * [\_\_init\_\_](#jukebox.playlistgenerator.PlaylistCollector.__init__)
    * [set\_exclusion\_endings](#jukebox.playlistgenerator.PlaylistCollector.set_exclusion_endings)
    * [get\_directory\_content](#jukebox.playlistgenerator.PlaylistCollector.get_directory_content)
    * [parse](#jukebox.playlistgenerator.PlaylistCollector.parse)
* [jukebox.api.events](#jukebox.api.events)
  * [EventBroker](#jukebox.api.events.EventBroker)
    * [publish](#jukebox.api.events.EventBroker.publish)
  * [parse\_subscription\_command](#jukebox.api.events.parse_subscription_command)
* [jukebox.api](#jukebox.api)
* [jukebox.api.fastapi\_server](#jukebox.api.fastapi_server)
  * [BodySizeLimit](#jukebox.api.fastapi_server.BodySizeLimit)
  * [FastApiServer](#jukebox.api.fastapi_server.FastApiServer)
* [jukebox.api.webapp\_static](#jukebox.api.webapp_static)
  * [register\_webapp\_routes](#jukebox.api.webapp_static.register_webapp_routes)
* [jukebox.version](#jukebox.version)
  * [version](#jukebox.version.version)
  * [version\_info](#jukebox.version.version_info)
* [jukebox.cfghandler](#jukebox.cfghandler)
  * [ConfigHandler](#jukebox.cfghandler.ConfigHandler)
    * [loaded\_from](#jukebox.cfghandler.ConfigHandler.loaded_from)
    * [get](#jukebox.cfghandler.ConfigHandler.get)
    * [setdefault](#jukebox.cfghandler.ConfigHandler.setdefault)
    * [getn](#jukebox.cfghandler.ConfigHandler.getn)
    * [setn](#jukebox.cfghandler.ConfigHandler.setn)
    * [setndefault](#jukebox.cfghandler.ConfigHandler.setndefault)
    * [config\_dict](#jukebox.cfghandler.ConfigHandler.config_dict)
    * [is\_modified](#jukebox.cfghandler.ConfigHandler.is_modified)
    * [clear\_modified](#jukebox.cfghandler.ConfigHandler.clear_modified)
    * [save](#jukebox.cfghandler.ConfigHandler.save)
    * [load](#jukebox.cfghandler.ConfigHandler.load)
  * [get\_handler](#jukebox.cfghandler.get_handler)
  * [load\_yaml](#jukebox.cfghandler.load_yaml)
  * [ensure\_default\_config](#jukebox.cfghandler.ensure_default_config)
  * [write\_yaml](#jukebox.cfghandler.write_yaml)
* [jukebox.timers](#jukebox.timers)
  * [Timers](#jukebox.timers.Timers)
    * [list\_timers](#jukebox.timers.Timers.list_timers)
    * [start\_timer](#jukebox.timers.Timers.start_timer)
    * [cancel](#jukebox.timers.Timers.cancel)
    * [toggle](#jukebox.timers.Timers.toggle)
* [jukebox.audio\_output](#jukebox.audio_output)
  * [scale\_volume](#jukebox.audio_output.scale_volume)
  * [AudioSink](#jukebox.audio_output.AudioSink)
  * [PortAudioSink](#jukebox.audio_output.PortAudioSink)
  * [play\_file](#jukebox.audio_output.play_file)
* [jukebox.core\_modules](#jukebox.core_modules)
* [jukebox.input\_devices](#jukebox.input_devices)
  * [Evdev](#jukebox.input_devices.Evdev)
    * [key\_downs](#jukebox.input_devices.Evdev.key_downs)
  * [InputDevices](#jukebox.input_devices.InputDevices)
    * [list\_devices](#jukebox.input_devices.InputDevices.list_devices)
* [jukebox.multitimer](#jukebox.multitimer)
  * [MultiTimer](#jukebox.multitimer.MultiTimer)
    * [cancel](#jukebox.multitimer.MultiTimer.cancel)
    * [trigger](#jukebox.multitimer.MultiTimer.trigger)
    * [run](#jukebox.multitimer.MultiTimer.run)
  * [GenericTimerClass](#jukebox.multitimer.GenericTimerClass)
    * [start](#jukebox.multitimer.GenericTimerClass.start)
    * [cancel](#jukebox.multitimer.GenericTimerClass.cancel)
    * [cancel\_generation](#jukebox.multitimer.GenericTimerClass.cancel_generation)
    * [toggle](#jukebox.multitimer.GenericTimerClass.toggle)
    * [trigger](#jukebox.multitimer.GenericTimerClass.trigger)
    * [is\_alive](#jukebox.multitimer.GenericTimerClass.is_alive)
    * [get\_timeout](#jukebox.multitimer.GenericTimerClass.get_timeout)
    * [set\_timeout](#jukebox.multitimer.GenericTimerClass.set_timeout)
    * [publish](#jukebox.multitimer.GenericTimerClass.publish)
    * [get\_state](#jukebox.multitimer.GenericTimerClass.get_state)
    * [close](#jukebox.multitimer.GenericTimerClass.close)
  * [GenericEndlessTimerClass](#jukebox.multitimer.GenericEndlessTimerClass)
    * [get\_state](#jukebox.multitimer.GenericEndlessTimerClass.get_state)
* [jukebox.legacy\_actions](#jukebox.legacy_actions)
  * [convert](#jukebox.legacy_actions.convert)
  * [bind\_action](#jukebox.legacy_actions.bind_action)
* [jukebox.daemon](#jukebox.daemon)
  * [DEFAULT\_CONFIG\_TEMPLATE](#jukebox.daemon.DEFAULT_CONFIG_TEMPLATE)
  * [shutdown\_signal](#jukebox.daemon.shutdown_signal)
  * [log\_active\_threads](#jukebox.daemon.log_active_threads)
  * [JukeBox](#jukebox.daemon.JukeBox)
    * [signal\_handler](#jukebox.daemon.JukeBox.signal_handler)
* [jukebox.misc.simplecolors](#jukebox.misc.simplecolors)
  * [Colors](#jukebox.misc.simplecolors.Colors)
  * [resolve](#jukebox.misc.simplecolors.resolve)
  * [print](#jukebox.misc.simplecolors.print)
* [jukebox.misc](#jukebox.misc)
  * [recursive\_chmod](#jukebox.misc.recursive_chmod)
  * [flatten](#jukebox.misc.flatten)
  * [getattr\_hierarchical](#jukebox.misc.getattr_hierarchical)
* [jukebox.misc.inputminus](#jukebox.misc.inputminus)
  * [input\_int](#jukebox.misc.inputminus.input_int)
  * [input\_yesno](#jukebox.misc.inputminus.input_yesno)
* [jukebox.misc.loggingext](#jukebox.misc.loggingext)
  * [ColorFilter](#jukebox.misc.loggingext.ColorFilter)
    * [\_\_init\_\_](#jukebox.misc.loggingext.ColorFilter.__init__)
  * [PubStream](#jukebox.misc.loggingext.PubStream)
  * [PubStreamHandler](#jukebox.misc.loggingext.PubStreamHandler)
* [jukebox.contract.interfaces](#jukebox.contract.interfaces)
* [jukebox.contract.declarations](#jukebox.contract.declarations)
  * [OperationSpec](#jukebox.contract.declarations.OperationSpec)
    * [kind](#jukebox.contract.declarations.OperationSpec.kind)
  * [action](#jukebox.contract.declarations.action)
  * [query](#jukebox.contract.declarations.query)
  * [EventSpec](#jukebox.contract.declarations.EventSpec)
  * [ExtensionPoint](#jukebox.contract.declarations.ExtensionPoint)
    * [on\_register](#jukebox.contract.declarations.ExtensionPoint.on_register)
  * [ExtensionPointSpec](#jukebox.contract.declarations.ExtensionPointSpec)
  * [Operation](#jukebox.contract.declarations.Operation)
    * [validate\_args](#jukebox.contract.declarations.Operation.validate_args)
* [jukebox.contract.catalog](#jukebox.contract.catalog)
  * [ActionCatalog](#jukebox.contract.catalog.ActionCatalog)
    * [validate](#jukebox.contract.catalog.ActionCatalog.validate)
* [jukebox.contract.context](#jukebox.contract.context)
  * [ModuleConfig](#jukebox.contract.context.ModuleConfig)
  * [ModuleProxy](#jukebox.contract.context.ModuleProxy)
  * [Context](#jukebox.contract.context.Context)
    * [lock](#jukebox.contract.context.Context.lock)
    * [subscribe](#jukebox.contract.context.Context.subscribe)
* [jukebox.contract.routes](#jukebox.contract.routes)
* [jukebox.contract.manager](#jukebox.contract.manager)
  * [discover\_plugins](#jukebox.contract.manager.discover_plugins)
  * [ModuleHandle](#jukebox.contract.manager.ModuleHandle)
  * [ModuleManager](#jukebox.contract.manager.ModuleManager)
    * [\_\_init\_\_](#jukebox.contract.manager.ModuleManager.__init__)
* [jukebox.contract.module](#jukebox.contract.module)
  * [Module](#jukebox.contract.module.Module)
    * [concurrency](#jukebox.contract.module.Module.concurrency)
    * [ready](#jukebox.contract.module.Module.ready)
    * [extra\_routes](#jukebox.contract.module.Module.extra_routes)
  * [CoreModule](#jukebox.contract.module.CoreModule)
  * [Plugin](#jukebox.contract.module.Plugin)
* [jukebox.contract.version](#jukebox.contract.version)
  * [CONTRACT\_VERSION](#jukebox.contract.version.CONTRACT_VERSION)
* [jukebox.contract](#jukebox.contract)
* [jukebox.contract.snapshots](#jukebox.contract.snapshots)
  * [check\_target](#jukebox.contract.snapshots.check_target)
* [jukebox.contract.errors](#jukebox.contract.errors)
  * [ContractError](#jukebox.contract.errors.ContractError)
  * [OperationError](#jukebox.contract.errors.OperationError)
  * [ActionError](#jukebox.contract.errors.ActionError)
* [jukebox.system](#jukebox.system)
  * [cpu\_temperature](#jukebox.system.cpu_temperature)
  * [ip\_addresses](#jukebox.system.ip_addresses)
  * [System](#jukebox.system.System)
    * [log](#jukebox.system.System.log)
    * [get\_info](#jukebox.system.System.get_info)
    * [get\_health](#jukebox.system.System.get_health)
    * [get\_ip\_addresses](#jukebox.system.System.get_ip_addresses)
    * [say\_my\_ip](#jukebox.system.System.say_my_ip)
    * [restart\_service](#jukebox.system.System.restart_service)
    * [get\_log](#jukebox.system.System.get_log)
    * [get\_app\_settings](#jukebox.system.System.get_app_settings)
    * [set\_app\_settings](#jukebox.system.System.set_app_settings)
    * [noop](#jukebox.system.System.noop)
* [jukebox.player.coordinator](#jukebox.player.coordinator)
  * [PlayerCoordinator](#jukebox.player.coordinator.PlayerCoordinator)
    * [\_\_init\_\_](#jukebox.player.coordinator.PlayerCoordinator.__init__)
    * [register\_backend](#jukebox.player.coordinator.PlayerCoordinator.register_backend)
    * [set\_default\_backend](#jukebox.player.coordinator.PlayerCoordinator.set_default_backend)
    * [select\_backend](#jukebox.player.coordinator.PlayerCoordinator.select_backend)
    * [play\_files](#jukebox.player.coordinator.PlayerCoordinator.play_files)
* [jukebox.player.module](#jukebox.player.module)
  * [Player](#jukebox.player.module.Player)
    * [play](#jukebox.player.module.Player.play)
    * [pause](#jukebox.player.module.Player.pause)
    * [toggle](#jukebox.player.module.Player.toggle)
    * [next](#jukebox.player.module.Player.next)
    * [prev](#jukebox.player.module.Player.prev)
    * [stop\_playback](#jukebox.player.module.Player.stop_playback)
    * [seek](#jukebox.player.module.Player.seek)
    * [shuffle](#jukebox.player.module.Player.shuffle)
    * [repeat](#jukebox.player.module.Player.repeat)
    * [rewind](#jukebox.player.module.Player.rewind)
    * [replay](#jukebox.player.module.Player.replay)
    * [replay\_if\_stopped](#jukebox.player.module.Player.replay_if_stopped)
    * [resume](#jukebox.player.module.Player.resume)
    * [play\_folder](#jukebox.player.module.Player.play_folder)
    * [play\_card](#jukebox.player.module.Player.play_card)
    * [play\_single](#jukebox.player.module.Player.play_single)
    * [play\_album](#jukebox.player.module.Player.play_album)
    * [queue\_load](#jukebox.player.module.Player.queue_load)
    * [update](#jukebox.player.module.Player.update)
    * [update\_wait](#jukebox.player.module.Player.update_wait)
    * [playerstatus](#jukebox.player.module.Player.playerstatus)
    * [get\_volume](#jukebox.player.module.Player.get_volume)
    * [set\_volume](#jukebox.player.module.Player.set_volume)
    * [playlistinfo](#jukebox.player.module.Player.playlistinfo)
    * [get\_current\_song](#jukebox.player.module.Player.get_current_song)
    * [get\_player\_type\_and\_version](#jukebox.player.module.Player.get_player_type_and_version)
    * [list\_backends](#jukebox.player.module.Player.list_backends)
    * [get\_active\_backend](#jukebox.player.module.Player.get_active_backend)
    * [get\_default\_backend](#jukebox.player.module.Player.get_default_backend)
    * [select\_backend](#jukebox.player.module.Player.select_backend)
* [jukebox.player.status](#jukebox.player.status)
  * [status\_from\_backend](#jukebox.player.status.status_from_backend)
* [jukebox.player](#jukebox.player)
  * [MusicLibPath](#jukebox.player.MusicLibPath)
  * [get\_music\_library\_path](#jukebox.player.get_music_library_path)
* [jukebox.player.backend](#jukebox.player.backend)
  * [PlayerBackend](#jukebox.player.backend.PlayerBackend)
    * [set\_status\_callback](#jukebox.player.backend.PlayerBackend.set_status_callback)
    * [play\_files](#jukebox.player.backend.PlayerBackend.play_files)
* [jukebox.player.backends.local\_audio](#jukebox.player.backends.local_audio)
  * [PlayerLocalAudio](#jukebox.player.backends.local_audio.PlayerLocalAudio)
    * [rewind](#jukebox.player.backends.local_audio.PlayerLocalAudio.rewind)
    * [replay](#jukebox.player.backends.local_audio.PlayerLocalAudio.replay)
* [jukebox.player.backends](#jukebox.player.backends)

<a id="jukebox"></a>

# jukebox

<a id="jukebox.utils"></a>

# jukebox.utils

Common utility functions


<a id="jukebox.utils.get_config_action"></a>

#### get\_config\_action

```python
def get_config_action(cfg, section, option, default, valid_actions_dict,
                      logger)
```

Looks up the given {section}.{option} config option and returns

the associated entry from valid_actions_dict, if valid. Falls back to the given
default otherwise.


<a id="jukebox.utils.get_git_state"></a>

#### get\_git\_state

```python
def get_git_state()
```

Return git state information for the current branch


<a id="jukebox.jingle"></a>

# jukebox.jingle

The jingle core module: startup and shutdown sounds, and playing a sound on demand.


<a id="jukebox.jingle.Jingle"></a>

## Jingle Objects

```python
class Jingle(CoreModule)
```

Plays the startup sound when ready and the shutdown sound when stopping.


<a id="jukebox.jingle.Jingle.play"></a>

#### play

```python
@action()
def play(sound: str) -> None
```

Play a sound file (path relative to the jukebox directory or absolute).


<a id="jukebox.library.index"></a>

# jukebox.library.index

SQLite index of the music library: tags and durations read with mutagen.

Songs are keyed by their path relative to the music library root. A scan only re-reads files whose
modification time or size changed.


<a id="jukebox.library.index.read_tags"></a>

#### read\_tags

```python
def read_tags(path: Path) -> Dict[str, Any]
```

Title, artist, album, albumartist, track, disc and duration of an audio file (missing: None).


<a id="jukebox.library.index.LibraryIndex"></a>

## LibraryIndex Objects

```python
class LibraryIndex()
```

<a id="jukebox.library.index.LibraryIndex.relative"></a>

#### relative

```python
def relative(song_url: str) -> Optional[str]
```

``song_url`` (absolute below the root, or relative to it) as index key, else None.


<a id="jukebox.library.index.LibraryIndex.scan"></a>

#### scan

```python
def scan() -> ScanResult
```

Bring the index in line with the files on disk. Concurrent calls run one after another.


<a id="jukebox.library.index.LibraryIndex.albums"></a>

#### albums

```python
def albums() -> List[Dict[str, Any]]
```

Albums grouped by album artist (falling back to the artist) and album title.


<a id="jukebox.library.files"></a>

# jukebox.library.files

Safe file operations within the music library.


<a id="jukebox.library.files.LibraryError"></a>

## LibraryError Objects

```python
class LibraryError(OperationError)
```

An expected library operation failure suitable for an HTTP response.


<a id="jukebox.library.files.resolve_library_path"></a>

#### resolve\_library\_path

```python
def resolve_library_path(root,
                         value,
                         *,
                         allow_root=True,
                         require_exists=False)
```

Resolve a relative or internal absolute path without escaping ``root``.


<a id="jukebox.library.files.UploadSession"></a>

## UploadSession Objects

```python
class UploadSession()
```

Write one upload to a temporary file and publish it atomically.


<a id="jukebox.library.files.MusicLibrary"></a>

## MusicLibrary Objects

```python
class MusicLibrary()
```

Perform validated mutations beneath a lazily resolved library root.


<a id="jukebox.library.module"></a>

# jukebox.library.module

The library core module: file management, index, metadata, cover art and library sources.


<a id="jukebox.library.module.LibrarySource"></a>

## LibrarySource Objects

```python
class LibrarySource(Protocol)
```

Further music a player backend or plugin can play (e.g. an mpd database, a streaming service).


<a id="jukebox.library.module.LibrarySource.describe"></a>

#### describe

```python
def describe() -> Dict[str, Any]
```

``{'id', 'label', 'views': [{'id', 'label', 'kind': 'items'|'folders', 'content_types'}]}``


<a id="jukebox.library.module.LibrarySource.list_items"></a>

#### list\_items

```python
def list_items(content_types: Optional[List[str]]) -> List[Dict[str, Any]]
```

Items (albums, playlists, ...) with ``albumartist``, ``album``, ``content_type``, ``content_uri``.


<a id="jukebox.library.module.LibrarySource.cover"></a>

#### cover

```python
def cover(song_url: str) -> Optional[str]
```

URL of the song's cover (absolute or relative to the web app), or None.


<a id="jukebox.library.module.song_from_source"></a>

#### song\_from\_source

```python
def song_from_source(provider: str, data: Dict[str, Any]) -> Song
```

A :class:`Song` from a source's song mapping (mpd style keys are understood).


<a id="jukebox.library.module.Library"></a>

## Library Objects

```python
class Library(CoreModule)
```

Music library: files, index with metadata, cover art; further sources plug in at ``library.sources``.


<a id="jukebox.library.module.Library.list_entries"></a>

#### list\_entries

```python
@query(path='/api/v1/library/entries')
def list_entries(folder: str) -> LibraryEntries
```

Files and folders in a library folder.


<a id="jukebox.library.module.Library.create_folder"></a>

#### create\_folder

```python
@action(path='/api/v1/library/folders', status_code=201)
def create_folder(parent: str, name: str) -> CreatedFolder
```

Create a folder in the library.


<a id="jukebox.library.module.Library.delete_entries"></a>

#### delete\_entries

```python
@action(method='DELETE', path='/api/v1/library/entries')
def delete_entries(paths: List[str]) -> DeletedEntries
```

Delete files and folders from the library.


<a id="jukebox.library.module.Library.refresh"></a>

#### refresh

```python
@action(path='/api/v1/library/refresh')
def refresh() -> ScanStarted
```

Rescan the library (and refresh all other sources).


<a id="jukebox.library.module.Library.list_sources"></a>

#### list\_sources

```python
@query(path='/sources')
def list_sources() -> List[SourceInfo]
```

The local library and every registered source, with their views.


<a id="jukebox.library.module.Library.list_items"></a>

#### list\_items

```python
@query(path='/items')
def list_items(provider: Optional[str] = None,
               content_types: Optional[List[str]] = None) -> List[LibraryItem]
```

Albums (and other items) of one source or all of them.


<a id="jukebox.library.module.Library.list_songs"></a>

#### list\_songs

```python
@query(path='/songs')
def list_songs(albumartist: str,
               album: str,
               content_uri: Optional[str] = None,
               provider: Optional[str] = None) -> List[Song]
```

Songs of an album, in track order.


<a id="jukebox.library.module.Library.get_song"></a>

#### get\_song

```python
@query(path='/song')
def get_song(song_url: str, provider: Optional[str] = None) -> Optional[Song]
```

Metadata of a single song, or null if it is unknown.


<a id="jukebox.library.module.Library.search"></a>

#### search

```python
@query(path='/search')
def search(query: str) -> List[Song]
```

Songs of the local library matching title, artist, album or path.


<a id="jukebox.library.module.Library.get_song_cover"></a>

#### get\_song\_cover

```python
@query(path='/cover/song')
def get_song_cover(song_url: str, provider: Optional[str] = None) -> CoverArt
```

Cover art URL of a song.


<a id="jukebox.library.module.Library.get_album_cover"></a>

#### get\_album\_cover

```python
@query(path='/cover/album')
def get_album_cover(albumartist: str,
                    album: str,
                    content_uri: Optional[str] = None,
                    provider: Optional[str] = None) -> CoverArt
```

Cover art URL of an album (the cover of its first song).


<a id="jukebox.library.module.Library.flush_covers"></a>

#### flush\_covers

```python
@action(path='/covers/flush')
def flush_covers() -> None
```

Delete all cached cover art; it is extracted again when needed.


<a id="jukebox.library.covers"></a>

# jukebox.library.covers

Cover art of songs: embedded pictures (MP3, FLAC, MP4, Ogg) or an image in the song's folder.


<a id="jukebox.library.covers.CoverCache"></a>

## CoverCache Objects

```python
class CoverCache()
```

Extracts covers into ``cache_dir`` once; names are content-independent hashes of the source.


<a id="jukebox.library.covers.CoverCache.cover_for"></a>

#### cover\_for

```python
def cover_for(song: Path) -> Optional[str]
```

File name in the cache of the song's cover, or None when it has none.


<a id="jukebox.library"></a>

# jukebox.library

The music library: file management, index, metadata and cover art.


<a id="jukebox.rfid.reader"></a>

# jukebox.rfid.reader

RFID reader framework: one thread per configured reader, card dispatch, card removal detection.

Hardware drivers register at the ``rfid.readers`` extension point. Readers are configured in the
reader config file (``rfid.reader_config``), each with the name of its driver under ``module``.


<a id="jukebox.rfid.reader.ReaderDriver"></a>

## ReaderDriver Objects

```python
class ReaderDriver(Protocol)
```

<a id="jukebox.rfid.reader.ReaderDriver.create_reader"></a>

#### create\_reader

```python
def create_reader(reader_cfg_key: str) -> Any
```

Return a reader for the reader config key: a context manager that iterates card ids

('' on timeout) and has ``stop()``.


<a id="jukebox.rfid.reader.CardRemovalTimer"></a>

## CardRemovalTimer Objects

```python
class CardRemovalTimer(threading.Thread)
```

Runs ``on_timeout`` once when the card has not been seen for about a second.


<a id="jukebox.rfid.reader.Rfid"></a>

## Rfid Objects

```python
class Rfid(CoreModule)
```

RFID readers: detect cards and run their actions.


<a id="jukebox.rfid.reader.Rfid.resolve_config_action"></a>

#### resolve\_config\_action

```python
def resolve_config_action(entry, where: str) -> Optional[Callable[[], Any]]
```

Turn a configured action (new or old format) into a callable, or None if invalid.


<a id="jukebox.rfid.reader.Rfid.list_readers"></a>

#### list\_readers

```python
@query(path='/readers')
def list_readers() -> Dict[str, str]
```

Configured readers and their driver.


<a id="jukebox.rfid.readerbase"></a>

# jukebox.rfid.readerbase

<a id="jukebox.rfid.readerbase.ReaderBaseClass"></a>

## ReaderBaseClass Objects

```python
class ReaderBaseClass(ABC)
```

Abstract Base Class for all Reader Classes to ensure common API

Look at template_new_reader.py for documentation how to integrate a new RFID reader


<a id="jukebox.rfid"></a>

# jukebox.rfid

<a id="jukebox.rfid.cards"></a>

# jukebox.rfid.cards

The RFID card database: which action a card triggers.

Entries are stored as ``action: <module>.<action>`` plus named ``args``. Entries in the pre-contract
format (alias or package/plugin/method) are converted once all modules are ready; the original
file is kept as a backup.


<a id="jukebox.rfid.cards.Cards"></a>

## Cards Objects

```python
class Cards(CoreModule)
```

Card database: register, list and delete cards.


<a id="jukebox.rfid.cards.Cards.list_cards"></a>

#### list\_cards

```python
@query(path='/api/v1/cards')
def list_cards() -> Dict[str, CardInfo]
```

All registered cards with their action and whether it is currently available.


<a id="jukebox.rfid.cards.Cards.get_card"></a>

#### get\_card

```python
@query(path='/api/v1/cards/{card_id}')
def get_card(card_id: str) -> Optional[CardEntry]
```

The card's entry, or null when it is unknown or its action is unavailable.


<a id="jukebox.rfid.cards.Cards.register_card"></a>

#### register\_card

```python
@action(path='/api/v1/cards')
def register_card(card_id: str,
                  action: str,
                  args: Optional[Dict[str, Any]] = None,
                  ignore_same_id_delay: bool = False,
                  ignore_card_removal_action: bool = False,
                  overwrite: bool = False) -> None
```

Register a card to trigger an action.


<a id="jukebox.rfid.cards.Cards.delete_card"></a>

#### delete\_card

```python
@action(method='DELETE', path='/api/v1/cards/{card_id}')
def delete_card(card_id: str) -> None
```

Delete a card.


<a id="jukebox.rfid.cardutils"></a>

# jukebox.rfid.cardutils

Readable descriptions of card database entries.


<a id="jukebox.rfid.cardutils.card_command_to_str"></a>

#### card\_command\_to\_str

```python
def card_command_to_str(entry: Mapping[str, Any],
                        long: bool = False) -> List[str]
```

``[action(args)]``, plus the card flags when ``long`` is set.


<a id="jukebox.volume"></a>

# jukebox.volume

The volume core module: volume, mute, soft maximum, output selection and fade-out.

The mixer is PulseAudio/PipeWire (via pulsectl) when a server is reachable, otherwise the volume of
the active player backend.


<a id="jukebox.volume.PlayerMixer"></a>

## PlayerMixer Objects

```python
class PlayerMixer()
```

Volume of the active player backend; no outputs to choose from.


<a id="jukebox.volume.PulseMixer"></a>

## PulseMixer Objects

```python
class PulseMixer()
```

PulseAudio/PipeWire default sink; ``volume_limit`` of an output scales 0..100 to 0..limit.


<a id="jukebox.volume.Volume"></a>

## Volume Objects

```python
class Volume(CoreModule)
```

Volume, mute, soft maximum and audio output.


<a id="jukebox.volume.Volume.get_volume"></a>

#### get\_volume

```python
@query(path='')
def get_volume() -> VolumeState
```

Current volume, mute state and soft maximum.


<a id="jukebox.volume.Volume.set_volume"></a>

#### set\_volume

```python
@action(method='PUT', path='')
def set_volume(volume: int) -> VolumeState
```

Set the volume (0-100, limited to the soft maximum).


<a id="jukebox.volume.Volume.change_volume"></a>

#### change\_volume

```python
@action(path='/change')
def change_volume(step: int = 5) -> VolumeState
```

Change the volume by ``step`` (negative to lower it).


<a id="jukebox.volume.Volume.mute"></a>

#### mute

```python
@action(path='/mute')
def mute(mute: Optional[bool] = None) -> VolumeState
```

Mute or unmute; toggles when ``mute`` is left out.


<a id="jukebox.volume.Volume.set_soft_max_volume"></a>

#### set\_soft\_max\_volume

```python
@action(method='PUT', path='/soft-max')
def set_soft_max_volume(max_volume: int) -> VolumeState
```

Limit the volume that can be set (0-100); lowers the current volume if needed.


<a id="jukebox.volume.Volume.get_outputs"></a>

#### get\_outputs

```python
@query(path='/outputs')
def get_outputs() -> OutputsState
```

Configured outputs that are available right now.


<a id="jukebox.volume.Volume.set_output"></a>

#### set\_output

```python
@action(method='PUT', path='/outputs/active')
def set_output(name: str) -> OutputsState
```

Switch the audio output.


<a id="jukebox.volume.Volume.toggle_output"></a>

#### toggle\_output

```python
@action(path='/outputs/toggle')
def toggle_output() -> OutputsState
```

Switch to the next available output.


<a id="jukebox.volume.Volume.fade_out"></a>

#### fade\_out

```python
@action(path='/fade-out')
def fade_out(seconds: float = 10.0) -> None
```

Lower the volume to zero over ``seconds``, stop playback, then restore the volume.


<a id="jukebox.nv_manager"></a>

# jukebox.nv\_manager

<a id="jukebox.publishing.bus"></a>

# jukebox.publishing.bus

Thread-safe in-process pub/sub bus with last-value caching.

Replaces the ZMQ-based Publisher/PublishServer pair (see
documentation/developers/roadmap-core-architecture.md, "Simplify away ZMQ and nginx"): this is a
single-process app, so a plain thread-safe broadcast is enough -- ZMQ solved a distributed-systems
problem (many independent processes, high throughput) that doesn't apply here.

`publish()` can be called from any thread (components run in RFID reader threads, timer threads,
etc.); subscriber callbacks are invoked synchronously on the publishing thread, so they must be
fast and must not block. The FastAPI bridge hands off to its own event loop via
`asyncio.run_coroutine_threadsafe` rather than doing any real work in the callback itself.


<a id="jukebox.publishing.bus.EventBus"></a>

## EventBus Objects

```python
class EventBus()
```

<a id="jukebox.publishing.bus.EventBus.publish"></a>

#### publish

```python
def publish(topic: str, payload: Optional[Any]) -> None
```

Publish `payload` for `topic`. `payload=None` revokes the topic.


<a id="jukebox.publishing.bus.EventBus.resend"></a>

#### resend

```python
def resend(topic_prefix: str = '') -> None
```

Re-send all cached topics under `topic_prefix` to every subscriber.


<a id="jukebox.publishing.bus.EventBus.cache_snapshot"></a>

#### cache\_snapshot

```python
def cache_snapshot() -> Dict[str, Any]
```

A shallow copy of the full last-value cache, for a client that just subscribed.


<a id="jukebox.publishing"></a>

# jukebox.publishing

The process-wide event bus. Modules publish through their ``Context``, not directly.


<a id="jukebox.publishing.get_bus"></a>

#### get\_bus

```python
def get_bus() -> EventBus
```

The shared, thread-safe event bus.


<a id="jukebox.playlistgenerator"></a>

# jukebox.playlistgenerator

Playlists are build from directory content in the following way:

a directory is parsed and files are added to the playlist in the following way

1. files are added in alphabetic order
2. files ending with ``*livestream.txt`` are unpacked and the containing URL(s) are added verbatim to the playlist
3. files ending with ``*podcast.txt`` are unpacked and the containing Podcast URL(s) are expanded and added to the playlist
4. files ending with ``*.m3u`` are treated as folder playlist. Regular folder processing is suspended and the playlist
   is build solely from the ``*.m3u`` content. Only the alphabetically first ``*.m3u`` is processed. URLs are added verbatim
   to the playlist except for ``*.xml`` and ``*.podcast`` URLS, which are expanded first

An directory may contain a mixed set of files and multiple ``*.txt`` files, e.g.

    01-livestream.txt
    02-livestream.txt
    music.mp3
    podcast.txt

All files are treated as music files and are added to the playlist, except those:

 * starting with ``.``,
 * not having a file ending, i.e. do not contain a ``.``,
 * ending with ``.txt``,
 * ending with ``.m3u``,
 * ending with one of the excluded file endings in :attr:`PlaylistCollector._exclude_endings`

In recursive mode, the playlist is generated by concatenating all sub-folder playlists. Sub-folders are parsed
in alphabetic order. Symbolic links are being followed. The above rules are enforced on a per-folder bases.
This means, one ``*.m3u`` file per sub-folder is processed (if present).

In ``*.txt`` and ``*.m3u`` files, all lines starting with ``#`` are ignored.


<a id="jukebox.playlistgenerator.TYPE_DECODE"></a>

#### TYPE\_DECODE

Types if file entires in parsed directory


<a id="jukebox.playlistgenerator.PlaylistCollector"></a>

## PlaylistCollector Objects

```python
class PlaylistCollector()
```

Build a playlist from directory(s)

This class is intended to be used with an absolute path to the music library::

    plc = PlaylistCollector('/home/chris/music')
    plc.parse('Traumfaenger')
    print(f"res = {plc}")

But it can also be used with relative paths from current working directory::

    plc = PlaylistCollector('.')
    plc.parse('../../../../music/Traumfaenger')
    print(f"res = {plc}")

The file ending exclusion list :attr:`PlaylistCollector._exclude_endings` is a class variable for performance reasons.
If changed it will affect all instances. For modifications always call :func:`set_exclusion_endings`.


<a id="jukebox.playlistgenerator.PlaylistCollector.__init__"></a>

#### \_\_init\_\_

```python
def __init__(music_library_base_path='/')
```

Initialize the playlist generator with music_library_base_path

**Arguments**:

- `music_library_base_path`: Base path the the music library. This is used to locate the file in the disk
but is omitted when generating the playlist entries. I.e. all files in the playlist are relative to this base dir

<a id="jukebox.playlistgenerator.PlaylistCollector.set_exclusion_endings"></a>

#### set\_exclusion\_endings

```python
@classmethod
def set_exclusion_endings(cls, endings: List[str])
```

Set the class-wide file ending exclusion list

See :attr:`PlaylistCollector._exclude_endings`


<a id="jukebox.playlistgenerator.PlaylistCollector.get_directory_content"></a>

#### get\_directory\_content

```python
def get_directory_content(path='.')
```

Parse the folder ``path`` and create a content list. Depth is always the current level

**Arguments**:

- `path`: Path to folder **relative** to ``music_library_base_path``

**Returns**:

[ { type: 'directory', name: 'Simone', path: '/some/path/to/Simone' }, {...} ]
where type is one of :attr:`TYPE_DECODE`

<a id="jukebox.playlistgenerator.PlaylistCollector.parse"></a>

#### parse

```python
def parse(path='.', recursive=False)
```

Parse the folder ``path`` and create a playlist from its content

**Arguments**:

- `path`: Path to folder **relative** to ``music_library_base_path``
- `recursive`: Parse folder recursivley, or stay in top-level folder

<a id="jukebox.api.events"></a>

# jukebox.api.events

Transport-neutral pieces of the browser events-over-websocket bridge.

Split out of the old Tornado bridge (`jukebox.api.server`, removed once `jukebox.api.fastapi_server`
became the sole HTTP/WebSocket bridge) so nothing here depends on a specific web framework.


<a id="jukebox.api.events.EventBroker"></a>

## EventBroker Objects

```python
class EventBroker()
```

Maintain browser subscriptions, backed by the shared :class:`jukebox.publishing.bus.EventBus`.

Register :meth:`publish` as a bus subscriber callback (``bus.register(broker.publish)``); the
bus already delivers `payload=None` for revocations and calls this from whatever thread
published, so no separate transport bridging is needed here.


<a id="jukebox.api.events.EventBroker.publish"></a>

#### publish

```python
def publish(topic, payload)
```

Bus subscriber callback. `payload=None` means the topic was revoked.


<a id="jukebox.api.events.parse_subscription_command"></a>

#### parse\_subscription\_command

```python
def parse_subscription_command(command)
```

Validate a decoded events-websocket command.

**Raises**:

- `ValueError`: if the command is not a well-formed subscribe/unsubscribe request

**Returns**:

``(command_type, topics)``

<a id="jukebox.api"></a>

# jukebox.api

HTTP and WebSocket API for browser clients.


<a id="jukebox.api.fastapi_server"></a>

# jukebox.api.fastapi\_server

FastAPI + uvicorn HTTP and WebSocket API server.

The sole browser-facing HTTP/WebSocket bridge. Serves health, the routes of the modules (see
jukebox.contract.routes), events-over-websocket and (see jukebox.api.webapp_static) the webapp's
static build + /logs -- this is the one thing reachable from the LAN, hence `api.bind_address`
defaulting to 0.0.0.0.

Handlers run on a multi-worker executor; each module guards itself (see the contract's threading
model), so a slow call doesn't serialize the rest of the API.


<a id="jukebox.api.fastapi_server.BodySizeLimit"></a>

## BodySizeLimit Objects

```python
class BodySizeLimit()
```

Reject request bodies above ``limit`` bytes with 413 (except for streaming upload paths).


<a id="jukebox.api.fastapi_server.FastApiServer"></a>

## FastApiServer Objects

```python
class FastApiServer(threading.Thread)
```

Run the browser API on an isolated asyncio event loop.


<a id="jukebox.api.webapp_static"></a>

# jukebox.api.webapp\_static

Serve the built webapp, its fallback pages, and the /logs directory directly from FastAPI.

Replaces nginx (see documentation/developers/roadmap-core-architecture.md, "Simplify away ZMQ and
nginx"): nginx's only jobs here were reverse-proxying /api/ to the browser bridge (now just
FastAPI itself, nothing to proxy to) and serving the webapp's static build, a "build
missing"/generic-404 fallback page, and a /logs directory listing. Small enough to do directly.

Deliberately matches the old `resources/default-settings/nginx.default` behavior rather than
adding new behavior (e.g. no SPA deep-link fallback to index.html for unknown paths -- nginx's
`try_files $uri $uri/ =404` didn't do that either, so neither does this).


<a id="jukebox.api.webapp_static.register_webapp_routes"></a>

#### register\_webapp\_routes

```python
def register_webapp_routes(app: FastAPI, *, build_dir: Path,
                           logs_dir: Path) -> None
```

Mount the webapp build's static assets, index.html, a generic 404, and /logs. Call once.


<a id="jukebox.version"></a>

# jukebox.version

<a id="jukebox.version.version"></a>

#### version

```python
def version()
```

Return the Jukebox version as a string


<a id="jukebox.version.version_info"></a>

#### version\_info

```python
def version_info()
```

Return the Jukebox version as a tuple of three numbers

If this is a development version, an identifier string will be appended after the third integer.


<a id="jukebox.cfghandler"></a>

# jukebox.cfghandler

This module handles global and local configuration data

The concept is that config handler is created and initialized once in the main thread::

    cfg = get_handler('global')
    load_yaml(cfg, 'filename.yaml')

In all other modules (in potentially different threads) the same handler is obtained and used by::

    cfg = get_handler('global')

This eliminates the need to pass an effectively global configuration handler by parameters across the entire design.
Handlers are identified by their name (in the above example *global*)

The function :func:`get_handler` is the main entry point to obtain a new or existing handler.


<a id="jukebox.cfghandler.ConfigHandler"></a>

## ConfigHandler Objects

```python
class ConfigHandler()
```

The configuration handler class

Don't instantiate directly. Always use :func:`get_handler`!

**Threads:**

All threads can read and write to the configuration data.
**Proper thread-safeness must be ensured** by the the thread modifying the data by acquiring the lock
Easiest and best way is to use the context handler::

    with cfg:
       cfg['key'] = 66
       cfg.setndefault('hello', value='world')

For a single function call, this is done implicitly. In this case, there is no need
to explicitly acquire the lock.

Alternatively, you can lock and release manually by using :func:`acquire` and :func:`release`
But be very sure to release the lock even in cases of errors an exceptions!
Else we have a deadlock.

Reading may be done without acquiring a lock. But be aware that when reading multiple values without locking, another
thread may intervene and modify some values in between! So, locking is still recommended.


<a id="jukebox.cfghandler.ConfigHandler.loaded_from"></a>

#### loaded\_from

```python
@property
def loaded_from() -> Optional[str]
```

Property to store filename from which the config was loaded


<a id="jukebox.cfghandler.ConfigHandler.get"></a>

#### get

```python
def get(key, *, default=None)
```

Enforce keyword on default to avoid accidental misuse when actually getn is wanted


<a id="jukebox.cfghandler.ConfigHandler.setdefault"></a>

#### setdefault

```python
def setdefault(key, *, value)
```

Enforce keyword on default to avoid accidental misuse when actually setndefault is wanted


<a id="jukebox.cfghandler.ConfigHandler.getn"></a>

#### getn

```python
def getn(*keys, default=None)
```

Get the value at arbitrary hierarchy depth. Return ``default`` if key not present

The *default* value is returned no matter at which hierarchy level the path aborts.
A hierarchy is considered as any type with a :func:`get` method.


<a id="jukebox.cfghandler.ConfigHandler.setn"></a>

#### setn

```python
def setn(*keys, value, hierarchy_type=None) -> None
```

Set the ``key: value`` pair at arbitrary hierarchy depth

All non-existing hierarchy levels are created.

**Arguments**:

- `keys`: Key hierarchy path through the nested levels
- `value`: The value to set
- `hierarchy_type`: The type for new hierarchy levels. If *None*, the top-level type
is used

<a id="jukebox.cfghandler.ConfigHandler.setndefault"></a>

#### setndefault

```python
def setndefault(*keys, value, hierarchy_type=None)
```

Set the ``key: value`` pair at arbitrary hierarchy depth unless the key already exists

All non-existing hierarchy levels are created.

**Arguments**:

- `keys`: Key hierarchy path through the nested levels
- `value`: The default value to set
- `hierarchy_type`: The type for new hierarchy levels. If *None*, the top-level type
is used

**Returns**:

The actual value or or the default value if key does not exit

<a id="jukebox.cfghandler.ConfigHandler.config_dict"></a>

#### config\_dict

```python
def config_dict(data)
```

Initialize configuration data from dict-like data structure

**Arguments**:

- `data`: configuration data

<a id="jukebox.cfghandler.ConfigHandler.is_modified"></a>

#### is\_modified

```python
def is_modified() -> bool
```

Check if the data has changed since the last load/store

> [!NOTE]
> This relies on the *__str__* representation of the underlying data structure
> In case of ruamel, this ignores comments and only looks at the data


<a id="jukebox.cfghandler.ConfigHandler.clear_modified"></a>

#### clear\_modified

```python
def clear_modified() -> None
```

Sets the current state as new baseline, clearing the is_modified state


<a id="jukebox.cfghandler.ConfigHandler.save"></a>

#### save

```python
def save(only_if_changed: bool = False) -> None
```

Save config back to the file it was loaded from

If you want to save to a different file, use :func:`write_yaml`.


<a id="jukebox.cfghandler.ConfigHandler.load"></a>

#### load

```python
def load(filename: str) -> None
```

Load YAML config file into memory


<a id="jukebox.cfghandler.get_handler"></a>

#### get\_handler

```python
def get_handler(name: str) -> ConfigHandler
```

Get a configuration data handler with the specified name, creating it

if it doesn't yet exit. If created, it is always created empty.

This is the main entry point for obtaining an configuration handler

**Arguments**:

- `name`: Name of the config handler

**Returns**:

`ConfigHandler`: The configuration data handler for *name*

<a id="jukebox.cfghandler.load_yaml"></a>

#### load\_yaml

```python
def load_yaml(cfg: ConfigHandler, filename: str) -> None
```

Load a yaml file into a ConfigHandler

**Arguments**:

- `cfg`: ConfigHandler instance
- `filename`: filename to yaml file

**Returns**:

None

<a id="jukebox.cfghandler.ensure_default_config"></a>

#### ensure\_default\_config

```python
def ensure_default_config(filename: str, template: str) -> None
```

Create `filename` from `template` if it doesn't exist yet (creating parent directories as

needed). Lets a fresh checkout/install start with sensible defaults instead of requiring a
separate install step to have copied the template first.

**Arguments**:

- `filename`: path the config file is expected/wanted at
- `template`: path to the default template to copy from if `filename` is missing

**Returns**:

None

<a id="jukebox.cfghandler.write_yaml"></a>

#### write\_yaml

```python
def write_yaml(cfg: ConfigHandler,
               filename: str,
               only_if_changed: bool = False,
               *args,
               **kwargs) -> None
```

Writes ConfigHandler data to yaml file / sys.stdout

**Arguments**:

- `cfg`: ConfigHandler instance
- `filename`: filename to output file. If *sys.stdout*, output is written to console
- `only_if_changed`: Write file only, if ConfigHandler.is_modified()
- `args`: passed on to yaml.dump(...)
- `kwargs`: passed on to yaml.dump(...)

**Returns**:

None

<a id="jukebox.timers"></a>

# jukebox.timers

The timers core module: named countdowns that run an action when they expire.

Timers are configured under ``timers:``; each runs an action (``action``/``args``) after
``default_timeout_sec`` unless started with another duration. A timer whose action is not available
(e.g. its plugin is disabled) is listed, but can't be started.


<a id="jukebox.timers.Timers"></a>

## Timers Objects

```python
class Timers(CoreModule)
```

Countdown timers that run an action when they expire.


<a id="jukebox.timers.Timers.list_timers"></a>

#### list\_timers

```python
@query(path='')
def list_timers() -> List[TimerState]
```

All timers with their state.


<a id="jukebox.timers.Timers.start_timer"></a>

#### start\_timer

```python
@action(name='start', path='/start')
def start_timer(timer: str,
                wait_seconds: Optional[float] = None) -> TimerState
```

Start (or restart) a timer; ``wait_seconds`` defaults to the timer's configured timeout.


<a id="jukebox.timers.Timers.cancel"></a>

#### cancel

```python
@action(path='/cancel')
def cancel(timer: str) -> TimerState
```

Cancel a running timer.


<a id="jukebox.timers.Timers.toggle"></a>

#### toggle

```python
@action(path='/toggle')
def toggle(timer: str, wait_seconds: Optional[float] = None) -> TimerState
```

Start the timer if it is not running, cancel it otherwise.


<a id="jukebox.audio_output"></a>

# jukebox.audio\_output

PCM output through sounddevice/PortAudio, shared by the local_audio backend and the jingle.


<a id="jukebox.audio_output.scale_volume"></a>

#### scale\_volume

```python
def scale_volume(data: bytes, volume: int) -> bytes
```

Scale packed s16 PCM by volume (0-100). No-op at full volume (the common case).


<a id="jukebox.audio_output.AudioSink"></a>

## AudioSink Objects

```python
class AudioSink()
```

What a decoded track is written to. Exists so tests don't need a real audio device.


<a id="jukebox.audio_output.PortAudioSink"></a>

## PortAudioSink Objects

```python
class PortAudioSink(AudioSink)
```

Real output via sounddevice/PortAudio. Falls back to silent (no-op) if no device is

available -- e.g. the no-audio docker dev stack, or a CI box -- rather than raising and
killing the daemon.


<a id="jukebox.audio_output.play_file"></a>

#### play\_file

```python
def play_file(path: str,
              volume: int = 100,
              sink=None,
              should_stop=lambda: False) -> None
```

Decode ``path`` and play it to the end (or until ``should_stop()``), blocking.


<a id="jukebox.core_modules"></a>

# jukebox.core\_modules

The core modules the daemon always starts. Order is irrelevant, ``requires`` decides.


<a id="jukebox.input_devices"></a>

# jukebox.input\_devices

The input core module: keys of evdev input devices (USB buttons, keyboards, headset buttons) run actions.

Configured under ``input:``::

    input:
      media_keys: false          # play/pause/next/volume keys of any device (e.g. a Bluetooth headset)
      devices:
        joystick:
          device_name: DragonRise Inc.   Generic   USB
          exact: false           # substring match of the device name
          keys:
            BTN_TRIGGER: {action: player.toggle}
            297: {action: player.prev}


<a id="jukebox.input_devices.Evdev"></a>

## Evdev Objects

```python
class Evdev()
```

Access to the evdev library; replaced in tests.


<a id="jukebox.input_devices.Evdev.key_downs"></a>

#### key\_downs

```python
def key_downs(device, stop: threading.Event)
```

Yield key codes pressed on ``device`` until ``stop`` is set; raises OSError on disconnect.


<a id="jukebox.input_devices.InputDevices"></a>

## InputDevices Objects

```python
class InputDevices(CoreModule)
```

Keys of input devices run actions.


<a id="jukebox.input_devices.InputDevices.list_devices"></a>

#### list\_devices

```python
@query(path='/devices')
def list_devices() -> List[DeviceState]
```

Configured input devices and whether they are connected.


<a id="jukebox.multitimer"></a>

# jukebox.multitimer

Threaded one-shot and fixed-delay periodic timers.


<a id="jukebox.multitimer.MultiTimer"></a>

## MultiTimer Objects

```python
class MultiTimer(threading.Thread)
```

Execute a callback after each fixed-delay interval.

Limited timers count iterations down from ``iterations - 1`` to zero.
Negative iteration counts repeat until cancellation.


<a id="jukebox.multitimer.MultiTimer.cancel"></a>

#### cancel

```python
def cancel()
```

Stop the timer and wake its worker.


<a id="jukebox.multitimer.MultiTimer.trigger"></a>

#### trigger

```python
def trigger()
```

Trigger the next callback immediately.


<a id="jukebox.multitimer.MultiTimer.run"></a>

#### run

```python
def run()
```

Run until all iterations complete, cancellation, or callback failure.


<a id="jukebox.multitimer.GenericTimerClass"></a>

## GenericTimerClass Objects

```python
class GenericTimerClass()
```

A race-safe, single-execution timer. ``on_change(state)`` is called on every state change.


<a id="jukebox.multitimer.GenericTimerClass.start"></a>

#### start

```python
def start(wait_seconds: Optional[float] = None, restart: bool = True)
```

Start the timer, atomically replacing an active generation by default.


<a id="jukebox.multitimer.GenericTimerClass.cancel"></a>

#### cancel

```python
def cancel()
```

Cancel the active generation.


<a id="jukebox.multitimer.GenericTimerClass.cancel_generation"></a>

#### cancel\_generation

```python
def cancel_generation(worker)
```

Cancel one worker without affecting a newer generation.


<a id="jukebox.multitimer.GenericTimerClass.toggle"></a>

#### toggle

```python
def toggle()
```

Toggle between active and disabled states.


<a id="jukebox.multitimer.GenericTimerClass.trigger"></a>

#### trigger

```python
def trigger()
```

Trigger the active generation immediately.


<a id="jukebox.multitimer.GenericTimerClass.is_alive"></a>

#### is\_alive

```python
def is_alive() -> bool
```

Return whether a timer generation is logically active.


<a id="jukebox.multitimer.GenericTimerClass.get_timeout"></a>

#### get\_timeout

```python
def get_timeout() -> float
```

Return the configured timeout in seconds.


<a id="jukebox.multitimer.GenericTimerClass.set_timeout"></a>

#### set\_timeout

```python
def set_timeout(wait_seconds: float) -> float
```

Set the timeout, atomically replacing an active generation.


<a id="jukebox.multitimer.GenericTimerClass.publish"></a>

#### publish

```python
def publish()
```

Publish the current timer state.


<a id="jukebox.multitimer.GenericTimerClass.get_state"></a>

#### get\_state

```python
def get_state() -> Dict[str, Any]
```

Return the timer state.


<a id="jukebox.multitimer.GenericTimerClass.close"></a>

#### close

```python
def close()
```

Permanently close this timer and join all active workers.


<a id="jukebox.multitimer.GenericEndlessTimerClass"></a>

## GenericEndlessTimerClass Objects

```python
class GenericEndlessTimerClass(GenericTimerClass)
```

A fixed-delay timer that repeats until cancellation.


<a id="jukebox.multitimer.GenericEndlessTimerClass.get_state"></a>

#### get\_state

```python
def get_state() -> Dict[str, Any]
```

Return the periodic timer state.


<a id="jukebox.legacy_actions"></a>

# jukebox.legacy\_actions

Conversion of pre-contract commands to action ids.

Before the core/plugin contract, card entries and config actions were stored either as an alias
(``alias: play_card``) or as ``package``/``plugin``/``method`` plus positional ``args`` and
``kwargs``. The contract stores ``action: <module>.<action>`` plus named ``args``.


<a id="jukebox.legacy_actions.convert"></a>

#### convert

```python
def convert(
        entry: Mapping,
        param_names=None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]
```

Convert a legacy command to ``{'action': ..., 'args': {...}}`` (card flags are kept).

**Arguments**:

- `param_names`: callable ``action_id -> list of parameter names`` or None if unknown;
needed only to name positional arguments

**Returns**:

``(converted, None)`` or ``(None, reason)``

<a id="jukebox.legacy_actions.bind_action"></a>

#### bind\_action

```python
def bind_action(catalog, entry, where: str,
                logger) -> Optional[Callable[[], Any]]
```

A callable running a configured action (either format), or None (logged) if it's invalid.


<a id="jukebox.daemon"></a>

# jukebox.daemon

<a id="jukebox.daemon.DEFAULT_CONFIG_TEMPLATE"></a>

#### DEFAULT\_CONFIG\_TEMPLATE

Template a missing configuration_file is created from on first run (see JukeBox.__init__).

Repository-root-relative, same convention as every other path in this codebase.


<a id="jukebox.daemon.shutdown_signal"></a>

#### shutdown\_signal

```python
def shutdown_signal() -> Optional[int]
```

The signal that started the shutdown (e.g. ``signal.SIGINT`` for Ctrl-C), None before.


<a id="jukebox.daemon.log_active_threads"></a>

#### log\_active\_threads

```python
@atexit.register
def log_active_threads()
```

This functions is registered with atexit very early, meaning it will be run very late. It is the best guess to

evaluate which Threads are still running (and probably shouldn't be)

This function is registered before all the components and their dependencies are loaded


<a id="jukebox.daemon.JukeBox"></a>

## JukeBox Objects

```python
class JukeBox()
```

<a id="jukebox.daemon.JukeBox.signal_handler"></a>

#### signal\_handler

```python
def signal_handler(esignal, frame)
```

Signal handler for orderly shutdown

On first Ctrl-C (or SIGTERM) orderly shutdown procedure is embarked upon. It gets allocated a time-out!
On third Ctrl-C (or SIGTERM), this is interrupted and there will be a hard exit!


<a id="jukebox.misc.simplecolors"></a>

# jukebox.misc.simplecolors

Zero 3rd-party dependency module to add colors to unix terminal output

Yes, there are modules out there to do the same and they have more features.
However, this is low-complexity and has zero dependencies


<a id="jukebox.misc.simplecolors.Colors"></a>

## Colors Objects

```python
class Colors()
```

Container class for all the colors as constants


<a id="jukebox.misc.simplecolors.resolve"></a>

#### resolve

```python
def resolve(color_name: str)
```

Resolve a color name into the respective color constant

**Arguments**:

- `color_name`: Name of the color

**Returns**:

color constant

<a id="jukebox.misc.simplecolors.print"></a>

#### print

```python
def print(color: Colors,
          *values,
          sep=' ',
          end='\n',
          file=sys.stdout,
          flush=False)
```

Drop-in replacement for print with color choice and auto color reset for convenience

Use just as a regular print function, but with first parameter as color


<a id="jukebox.misc"></a>

# jukebox.misc

<a id="jukebox.misc.recursive_chmod"></a>

#### recursive\_chmod

```python
def recursive_chmod(path, mode_files, mode_dirs)
```

Recursively change folder and file permissions

mode_files/mode dirs can be given in octal notation e.g. 0o777
flags from the stats module.

Reference: https://docs.python.org/3/library/os.html#os.chmod


<a id="jukebox.misc.flatten"></a>

#### flatten

```python
def flatten(iterable)
```

Flatten all levels of hierarchy in nested iterables


<a id="jukebox.misc.getattr_hierarchical"></a>

#### getattr\_hierarchical

```python
def getattr_hierarchical(obj: Any, name: str) -> Any
```

Like the builtin getattr, but descends though the hierarchy levels


<a id="jukebox.misc.inputminus"></a>

# jukebox.misc.inputminus

Zero 3rd-party dependency module for user prompting

Yes, there are modules out there to do the same and they have more features.
However, this is low-complexity and has zero dependencies


<a id="jukebox.misc.inputminus.input_int"></a>

#### input\_int

```python
def input_int(prompt,
              blank=None,
              min=None,
              max=None,
              prompt_color=None,
              prompt_hint=False) -> int
```

Request an integer input from user

**Arguments**:

- `prompt`: The prompt to display
- `blank`: Value to return when user just hits enter. Leave at None, if blank is invalid
- `min`: Minimum valid integer value (None disables this check)
- `max`: Maximum valid integer value (None disables this check)
- `prompt_color`: Color of the prompt. Color will be reset at end of prompt
- `prompt_hint`: Append a 'hint' with [min...max, default=xx] to end of prompt

**Returns**:

integer value read from user input

<a id="jukebox.misc.inputminus.input_yesno"></a>

#### input\_yesno

```python
def input_yesno(prompt,
                blank=None,
                prompt_color=None,
                prompt_hint=False) -> bool
```

Request a yes / no choice from user

Accepts multiple input for true/false and is case insensitive

**Arguments**:

- `prompt`: The prompt to display
- `blank`: Value to return when user just hits enter. Leave at None, if blank is invalid
- `prompt_color`: Color of the prompt. Color will be reset at end of prompt
- `prompt_hint`: Append a 'hint' with [y/n] to end of prompt. Default choice will be capitalized

**Returns**:

boolean value read from user input

<a id="jukebox.misc.loggingext"></a>

# jukebox.misc.loggingext

## Logger

We use a hierarchical Logger structure based on pythons logging module. It can be finely configured with a yaml file.

The top-level logger is called 'jb' (to make it short). In any module you may simple create a child-logger at any hierarchy
level below 'jb'. It will inherit settings from it's parent logger unless otherwise configured in the yaml file.
Hierarchy separator is the '.'. If the logger already exits, getLogger will return a reference to the same, else it will be
created on the spot.

Example: How to get logger and log away at your heart's content:

    >>> import logging
    >>> logger = logging.getLogger('jb.awesome_module')
    >>> logger.info('Started general awesomeness aura')

Example: YAML snippet, setting WARNING as default level everywhere and DEBUG for jb.awesome_module:

    loggers:
      jb:
        level: WARNING
        handlers: [console, debug_file_handler, error_file_handler]
        propagate: no
      jb.awesome_module:
        level: DEBUG


> [!NOTE]
> The name (and hierarchy path) of the logger can be arbitrary and must not necessarily match the module name (still makes
> sense).
> There can be multiple loggers per module, e.g. for special classes, to further control the amount of log output


<a id="jukebox.misc.loggingext.ColorFilter"></a>

## ColorFilter Objects

```python
class ColorFilter(logging.Filter)
```

This filter adds colors to the logger

It adds all colors from simplecolors by using the color name as new keyword,
i.e. use %(colorname)c or {colorname} in the formatter string

It also adds the keyword {levelnameColored} which is an auto-colored drop-in replacement
for the levelname depending on severity.

Don't forget to {reset} the color settings at the end of the string.


<a id="jukebox.misc.loggingext.ColorFilter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(enable=True, color_levelname=True)
```

**Arguments**:

- `enable`: Enable the coloring
- `color_levelname`: Enable auto-coloring when using the levelname keyword

<a id="jukebox.misc.loggingext.PubStream"></a>

## PubStream Objects

```python
class PubStream()
```

Stream handler wrapper around the publisher for logging.StreamHandler

Allows logging to send all log information (based on logging configuration)
to the Publisher.

> [!CAUTION]
> This can lead to recursions!
> Recursions come up when
> * Publish.send / EventBus.publish also emits logs, which cause a another send, which emits a log,
> which causes a send, ..... `jukebox.publishing.bus.EventBus` guards against this (caps it at one
> extra level instead of recursing indefinitely), but still avoid triggering it needlessly.
> * Publisher initialization emits logs, which need a Publisher instance to send logs

> [!IMPORTANT]
> To avoid endless recursions: The creation of a Publisher MUST NOT generate any log messages! Nor any of the
> functions in the send-function stack!


<a id="jukebox.misc.loggingext.PubStreamHandler"></a>

## PubStreamHandler Objects

```python
class PubStreamHandler(logging.StreamHandler)
```

Wrapper for logging.StreamHandler with stream = PubStream

This serves one purpose: In logger.yaml custom handlers
can be configured (which are automatically instantiated).
Using this Handler, we can output to PubStream whithout
support code to instantiate PubStream keeping this file generic


<a id="jukebox.contract.interfaces"></a>

# jukebox.contract.interfaces

Interface snapshots of modules and the framework contract, and the rules for version bumps.

A snapshot is a JSON description of everything another module or plugin can rely on. Comparing
the stored snapshot with the current one tells whether a change is compatible (minor bump) or
breaking (major bump). See documentation/developers/core-and-plugins.md, "Versioning".


<a id="jukebox.contract.declarations"></a>

# jukebox.contract.declarations

Declarations a module uses to describe its interface: operations, events, extension points.


<a id="jukebox.contract.declarations.OperationSpec"></a>

## OperationSpec Objects

```python
@dataclass(frozen=True)
class OperationSpec()
```

<a id="jukebox.contract.declarations.OperationSpec.kind"></a>

#### kind

'action' | 'query'


<a id="jukebox.contract.declarations.action"></a>

#### action

```python
def action(func: Optional[Callable] = None,
           *,
           method: str = 'POST',
           path: Optional[str] = None,
           exclusive: bool = True,
           name: Optional[str] = None,
           status_code: Optional[int] = None)
```

Declare a state-changing operation: REST route, card action and in-process call.

``name`` overrides the operation name (default: the method name), e.g. where the method name
would clash with the lifecycle methods ``start``/``stop``/``ready``. ``status_code`` replaces
the default HTTP status of a successful call (200, or 204 without a result).


<a id="jukebox.contract.declarations.query"></a>

#### query

```python
def query(func: Optional[Callable] = None,
          *,
          path: Optional[str] = None,
          exclusive: bool = True,
          name: Optional[str] = None)
```

Declare a read-only operation: GET route and in-process call, not card-triggerable.


<a id="jukebox.contract.declarations.EventSpec"></a>

## EventSpec Objects

```python
class EventSpec()
```

A declared event. Published through ``ctx.publish(spec, payload)`` as ``<module>.<name>``.


<a id="jukebox.contract.declarations.ExtensionPoint"></a>

## ExtensionPoint Objects

```python
class ExtensionPoint()
```

Named implementations of a protocol, registered by other modules.


<a id="jukebox.contract.declarations.ExtensionPoint.on_register"></a>

#### on\_register

```python
def on_register(listener: Callable[[str, Any], None]) -> None
```

Call ``listener(key, implementation)`` for every current and future registration.


<a id="jukebox.contract.declarations.ExtensionPointSpec"></a>

## ExtensionPointSpec Objects

```python
class ExtensionPointSpec()
```

Class-level declaration of an extension point; each module instance gets its own registry.


<a id="jukebox.contract.declarations.Operation"></a>

## Operation Objects

```python
class Operation()
```

An operation of a module class with its argument model and return type.


<a id="jukebox.contract.declarations.Operation.validate_args"></a>

#### validate\_args

```python
def validate_args(args: Optional[dict]) -> dict
```

Validate a mapping of arguments; return the coerced keyword arguments.


<a id="jukebox.contract.catalog"></a>

# jukebox.contract.catalog

Card-triggerable actions of all started modules, addressed by ``<module>.<action>``.


<a id="jukebox.contract.catalog.ActionCatalog"></a>

## ActionCatalog Objects

```python
class ActionCatalog()
```

<a id="jukebox.contract.catalog.ActionCatalog.validate"></a>

#### validate

```python
def validate(action_id: str, args: Optional[dict] = None) -> Dict[str, Any]
```

Check that ``action_id`` exists and ``args`` fit its signature. Returns coerced args.


<a id="jukebox.contract.context"></a>

# jukebox.contract.context

What a module sees of the rest of the system.


<a id="jukebox.contract.context.ModuleConfig"></a>

## ModuleConfig Objects

```python
class ModuleConfig()
```

A module's own section of the main config (``<name>`` for core, ``plugins.<name>`` for plugins).


<a id="jukebox.contract.context.ModuleProxy"></a>

## ModuleProxy Objects

```python
class ModuleProxy()
```

The contract surface of another module: its operations and extension points.


<a id="jukebox.contract.context.Context"></a>

## Context Objects

```python
class Context()
```

<a id="jukebox.contract.context.Context.lock"></a>

#### lock

```python
@property
def lock()
```

The module's own lock, for work outside operations (e.g. background threads).

A no-op context manager for ``concurrency = 'threadsafe'`` modules.


<a id="jukebox.contract.context.Context.subscribe"></a>

#### subscribe

```python
def subscribe(topic_prefix: str, callback: Callable[[str, Optional[Any]],
                                                    None]) -> None
```

Call ``callback(topic, payload)`` for every event under ``topic_prefix``; payload None = revoked.


<a id="jukebox.contract.routes"></a>

# jukebox.contract.routes

FastAPI routes generated from module operations, plus ``GET /api/v1/modules``.


<a id="jukebox.contract.manager"></a>

# jukebox.contract.manager

Discovers, orders, starts and stops core modules and enabled plugins.


<a id="jukebox.contract.manager.discover_plugins"></a>

#### discover\_plugins

```python
def discover_plugins() -> Dict[str, Callable[[], type]]
```

Installed plugins by entry-point name. Loading (importing) happens only when enabled.


<a id="jukebox.contract.manager.ModuleHandle"></a>

## ModuleHandle Objects

```python
class ModuleHandle()
```

A started (or starting) module instance plus its lock and context.


<a id="jukebox.contract.manager.ModuleManager"></a>

## ModuleManager Objects

```python
class ModuleManager()
```

<a id="jukebox.contract.manager.ModuleManager.__init__"></a>

#### \_\_init\_\_

```python
def __init__(core_modules: Sequence[Type[CoreModule]],
             cfg,
             bus,
             *,
             plugins: Optional[Dict[str, Callable[[], type]]] = None,
             strict: Optional[bool] = None)
```

**Arguments**:

- `core_modules`: core module classes (order doesn't matter, ``requires`` decides)
- `cfg`: the main config handler; plugins are enabled under its ``plugins`` key
- `bus`: the event bus
- `plugins`: installed plugins by name (default: entry points of ``jukebox.plugins``)
- `strict`: raise instead of log on invalid events (default: ``$JUKEBOX_STRICT``)

<a id="jukebox.contract.module"></a>

# jukebox.contract.module

Base classes for core modules and plugins.


<a id="jukebox.contract.module.Module"></a>

## Module Objects

```python
class Module()
```

Common base of :class:`CoreModule` and :class:`Plugin`. Not subclassed directly.


<a id="jukebox.contract.module.Module.concurrency"></a>

#### concurrency

'serialized': every operation runs under a per-module lock. 'threadsafe': no lock.


<a id="jukebox.contract.module.Module.ready"></a>

#### ready

```python
def ready() -> None
```

Called once every module has started, in start order. All actions are available now.


<a id="jukebox.contract.module.Module.extra_routes"></a>

#### extra\_routes

```python
def extra_routes(router) -> None
```

Escape hatch for routes the declarations can't express (e.g. streaming uploads).

Receives a FastAPI ``APIRouter``; paths should live under ``/api/v1/<name>``.


<a id="jukebox.contract.module.CoreModule"></a>

## CoreModule Objects

```python
class CoreModule(Module)
```

Always shipped, always running part of the jukebox.


<a id="jukebox.contract.module.Plugin"></a>

## Plugin Objects

```python
class Plugin(Module)
```

Separately installed, opt-in module. Declares which framework contract it targets.


<a id="jukebox.contract.version"></a>

# jukebox.contract.version

<a id="jukebox.contract.version.CONTRACT_VERSION"></a>

#### CONTRACT\_VERSION

Version of the framework contract (Module/CoreModule/Plugin, declarations, Context, lifecycle).

Major bump on breaking changes, minor bump on additions. Checked by test/contract snapshots.


<a id="jukebox.contract"></a>

# jukebox.contract

Contract shared by core modules and plugins. See documentation/developers/core-and-plugins.md.


<a id="jukebox.contract.snapshots"></a>

# jukebox.contract.snapshots

Check or update the stored interface snapshots of the framework, core modules and bundled plugins.

uv run python -m jukebox.contract.snapshots            # check (what CI runs via pytest)
uv run python -m jukebox.contract.snapshots --update   # write snapshots after a version bump


<a id="jukebox.contract.snapshots.check_target"></a>

#### check\_target

```python
def check_target(target: Target) -> Optional[str]
```

Return a problem description, or None when the stored snapshot matches.


<a id="jukebox.contract.errors"></a>

# jukebox.contract.errors

<a id="jukebox.contract.errors.ContractError"></a>

## ContractError Objects

```python
class ContractError(Exception)
```

A module violates the contract (declaration, dependency or version problem).


<a id="jukebox.contract.errors.OperationError"></a>

## OperationError Objects

```python
class OperationError(Exception)
```

Raised by an operation to report a client error with an HTTP status and error code.


<a id="jukebox.contract.errors.ActionError"></a>

## ActionError Objects

```python
class ActionError(Exception)
```

An action id or its arguments are invalid.


<a id="jukebox.system"></a>

# jukebox.system

The system core module: version, logs, system information and web app settings.


<a id="jukebox.system.cpu_temperature"></a>

#### cpu\_temperature

```python
def cpu_temperature() -> Optional[float]
```

CPU temperature in °C from the first thermal zone, None where there is none.


<a id="jukebox.system.ip_addresses"></a>

#### ip\_addresses

```python
def ip_addresses() -> List[str]
```

Non-loopback IPv4 addresses of this machine.


<a id="jukebox.system.System"></a>

## System Objects

```python
class System(CoreModule)
```

Version information, log files and web app settings.


<a id="jukebox.system.System.log"></a>

#### log

Published by jukebox.misc.loggingext.PubStreamHandler when configured in logger.yaml


<a id="jukebox.system.System.get_info"></a>

#### get\_info

```python
@query(path='/info')
def get_info() -> SystemInfo
```

Version, git state and start time of the jukebox.


<a id="jukebox.system.System.get_health"></a>

#### get\_health

```python
@query(path='/health')
def get_health() -> SystemHealth
```

CPU temperature (where available) and disk usage of the music library's file system.


<a id="jukebox.system.System.get_ip_addresses"></a>

#### get\_ip\_addresses

```python
@query(path='/ip-addresses')
def get_ip_addresses() -> IpAddresses
```

IPv4 addresses of this machine.


<a id="jukebox.system.System.say_my_ip"></a>

#### say\_my\_ip

```python
@action()
def say_my_ip() -> None
```

Speak the IP address (needs espeak).


<a id="jukebox.system.System.restart_service"></a>

#### restart\_service

```python
@action()
def restart_service() -> None
```

Restart the jukebox systemd user service.


<a id="jukebox.system.System.get_log"></a>

#### get\_log

```python
@query(path='/log')
def get_log(kind: Literal['debug', 'error'] = 'debug') -> str
```

Content of the debug or error log file of this run.


<a id="jukebox.system.System.get_app_settings"></a>

#### get\_app\_settings

```python
@query(path='/api/v1/settings')
def get_app_settings() -> AppSettings
```

Web app settings.


<a id="jukebox.system.System.set_app_settings"></a>

#### set\_app\_settings

```python
@action(method='PUT', path='/api/v1/settings')
def set_app_settings(settings: AppSettingsUpdate) -> None
```

Change web app settings; fields left out stay unchanged.


<a id="jukebox.system.System.noop"></a>

#### noop

```python
@action()
def noop(message: str = '') -> None
```

Do nothing (logs ``message`` as a warning if given).


<a id="jukebox.player.coordinator"></a>

# jukebox.player.coordinator

<a id="jukebox.player.coordinator.PlayerCoordinator"></a>

## PlayerCoordinator Objects

```python
class PlayerCoordinator()
```

Provider-neutral facade for playback and content backends.


<a id="jukebox.player.coordinator.PlayerCoordinator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(second_swipe_action: Optional[Callable[[], Any]] = None)
```

**Arguments**:

- `second_swipe_action`: runs on a second swipe of the same card instead of the
backend's own second-swipe behavior

<a id="jukebox.player.coordinator.PlayerCoordinator.register_backend"></a>

#### register\_backend

```python
def register_backend(name: str,
                     backend: Any,
                     make_active: bool = False) -> None
```

Register a backend, selecting the first registered backend by default.


<a id="jukebox.player.coordinator.PlayerCoordinator.set_default_backend"></a>

#### set\_default\_backend

```python
def set_default_backend(name: str) -> None
```

Make ``name`` the backend used for content without an explicit provider.


<a id="jukebox.player.coordinator.PlayerCoordinator.select_backend"></a>

#### select\_backend

```python
def select_backend(name: str)
```

Stop the current backend and select another registered backend.


<a id="jukebox.player.coordinator.PlayerCoordinator.play_files"></a>

#### play\_files

```python
def play_files(paths)
```

Play a list of songs (paths below the music library, absolute or relative).


<a id="jukebox.player.module"></a>

# jukebox.player.module

The player core module: playback through registered backends, typed status events.


<a id="jukebox.player.module.Player"></a>

## Player Objects

```python
class Player(CoreModule)
```

Playback of folders, songs and albums; backends plug in at ``player.backends``.


<a id="jukebox.player.module.Player.play"></a>

#### play

```python
@action(path='/play')
def play() -> None
```

Start or resume playback.


<a id="jukebox.player.module.Player.pause"></a>

#### pause

```python
@action(path='/pause')
def pause(state: int = 1) -> None
```

Pause (state=1) or resume (state=0).


<a id="jukebox.player.module.Player.toggle"></a>

#### toggle

```python
@action(path='/toggle')
def toggle() -> None
```

Toggle between play and pause.


<a id="jukebox.player.module.Player.next"></a>

#### next

```python
@action(path='/next')
def next() -> None
```

Skip to the next song.


<a id="jukebox.player.module.Player.prev"></a>

#### prev

```python
@action(path='/prev')
def prev() -> None
```

Go back to the previous song.


<a id="jukebox.player.module.Player.stop_playback"></a>

#### stop\_playback

```python
@action(name='stop', path='/stop')
def stop_playback() -> None
```

Stop playback.


<a id="jukebox.player.module.Player.seek"></a>

#### seek

```python
@action(path='/seek')
def seek(position: float) -> None
```

Jump to a position (seconds) in the current song.


<a id="jukebox.player.module.Player.shuffle"></a>

#### shuffle

```python
@action(path='/shuffle')
def shuffle(option: str = 'toggle') -> None
```

Shuffle mode: 'toggle', 'enable' or 'disable'.


<a id="jukebox.player.module.Player.repeat"></a>

#### repeat

```python
@action(path='/repeat')
def repeat(option: str = 'toggle') -> None
```

Repeat mode: 'toggle', 'enable', 'enable_repeat_single' or 'disable'.


<a id="jukebox.player.module.Player.rewind"></a>

#### rewind

```python
@action(path='/rewind')
def rewind() -> None
```

Restart the playlist from its first song.


<a id="jukebox.player.module.Player.replay"></a>

#### replay

```python
@action(path='/replay')
def replay() -> None
```

Replay the current folder from the start.


<a id="jukebox.player.module.Player.replay_if_stopped"></a>

#### replay\_if\_stopped

```python
@action(path='/replay-if-stopped')
def replay_if_stopped() -> None
```

Replay the current folder if playback has stopped.


<a id="jukebox.player.module.Player.resume"></a>

#### resume

```python
@action(path='/resume')
def resume() -> None
```

Resume the last played folder where it stopped.


<a id="jukebox.player.module.Player.play_folder"></a>

#### play\_folder

```python
@action(path='/folder')
def play_folder(folder: str, recursive: bool = False) -> None
```

Play a folder of the music library.


<a id="jukebox.player.module.Player.play_card"></a>

#### play\_card

```python
@action()
def play_card(folder: str, recursive: bool = False) -> None
```

Play a folder; a second swipe of the same card runs the second-swipe action.


<a id="jukebox.player.module.Player.play_single"></a>

#### play\_single

```python
@action(path='/song')
def play_single(song_url: str, provider: Optional[str] = None) -> None
```

Play a single song.


<a id="jukebox.player.module.Player.play_album"></a>

#### play\_album

```python
@action(path='/album')
def play_album(albumartist: str,
               album: str,
               content_uri: Optional[str] = None,
               provider: Optional[str] = None) -> None
```

Play an album of the library or of a backend's own catalog (``provider``).


<a id="jukebox.player.module.Player.queue_load"></a>

#### queue\_load

```python
@action(path='/queue')
def queue_load(folder: str) -> None
```

Load a folder into the queue without playing it.


<a id="jukebox.player.module.Player.update"></a>

#### update

```python
@action(path='/update')
def update() -> Any
```

Rescan the music library of the default backend.


<a id="jukebox.player.module.Player.update_wait"></a>

#### update\_wait

```python
@action(path='/update-wait')
def update_wait() -> Any
```

Rescan the music library and wait for it to finish.


<a id="jukebox.player.module.Player.playerstatus"></a>

#### playerstatus

```python
@query(path='/status')
def playerstatus() -> PlayerStatus
```

Current player status.


<a id="jukebox.player.module.Player.get_volume"></a>

#### get\_volume

```python
@query(path='/volume')
def get_volume() -> VolumeLevel
```

Current playback volume of the active backend.


<a id="jukebox.player.module.Player.set_volume"></a>

#### set\_volume

```python
@action(method='PUT', path='/volume')
def set_volume(volume: int) -> VolumeLevel
```

Set the playback volume of the active backend.


<a id="jukebox.player.module.Player.playlistinfo"></a>

#### playlistinfo

```python
@query(path='/playlist')
def playlistinfo() -> List[Dict[str, Any]]
```

The current queue.


<a id="jukebox.player.module.Player.get_current_song"></a>

#### get\_current\_song

```python
@query(path='/current-song')
def get_current_song(param: Optional[str] = None) -> Any
```

Details of the current song.


<a id="jukebox.player.module.Player.get_player_type_and_version"></a>

#### get\_player\_type\_and\_version

```python
@query(path='/type')
def get_player_type_and_version() -> str
```

Type and version of the active backend.


<a id="jukebox.player.module.Player.list_backends"></a>

#### list\_backends

```python
@query(path='/backends')
def list_backends() -> List[str]
```

Registered backends.


<a id="jukebox.player.module.Player.get_active_backend"></a>

#### get\_active\_backend

```python
@query(path='/backends/active')
def get_active_backend() -> BackendName
```

The backend playing right now.


<a id="jukebox.player.module.Player.get_default_backend"></a>

#### get\_default\_backend

```python
@query(path='/backends/default')
def get_default_backend() -> BackendName
```

The backend used for content without an explicit provider.


<a id="jukebox.player.module.Player.select_backend"></a>

#### select\_backend

```python
@action(method='PUT', path='/backends/active')
def select_backend(name: str) -> BackendName
```

Stop the current backend and switch to another one.


<a id="jukebox.player.status"></a>

# jukebox.player.status

Typed player status, independent of the backend that produced it.


<a id="jukebox.player.status.status_from_backend"></a>

#### status\_from\_backend

```python
def status_from_backend(raw: Mapping[str, Any], provider: str) -> PlayerStatus
```

Build a :class:`PlayerStatus` from a backend's raw (mpd-style) status mapping.


<a id="jukebox.player"></a>

# jukebox.player

<a id="jukebox.player.MusicLibPath"></a>

## MusicLibPath Objects

```python
class MusicLibPath()
```

Determine the music library directory.

Primarily from `player.music_library_path` config (backend-agnostic). Falls back to parsing
`music_directory` out of mpd.conf only when the mpd backend is active and no explicit path was
configured -- keeps existing mpd installs working without a migration step.


<a id="jukebox.player.get_music_library_path"></a>

#### get\_music\_library\_path

```python
def get_music_library_path()
```

Get the music library path


<a id="jukebox.player.backend"></a>

# jukebox.player.backend

Protocol a player backend implements to register at the ``player.backends`` extension point.

Optional capabilities (library browsing, cover art, rewind, ...) are looked up by name at call
time; a backend without them makes the corresponding operation answer 501.


<a id="jukebox.player.backend.PlayerBackend"></a>

## PlayerBackend Objects

```python
class PlayerBackend(Protocol)
```

<a id="jukebox.player.backend.PlayerBackend.set_status_callback"></a>

#### set\_status\_callback

```python
def set_status_callback(callback: Callable[[Mapping[str, Any]], None]) -> None
```

Receive the raw status mapping whenever it changes (only forwarded while active).


<a id="jukebox.player.backend.PlayerBackend.play_files"></a>

#### play\_files

```python
def play_files(paths: List[str]) -> None
```

Replace the queue with ``paths`` (absolute or relative to the music library) and play.


<a id="jukebox.player.backends.local_audio"></a>

# jukebox.player.backends.local\_audio

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


<a id="jukebox.player.backends.local_audio.PlayerLocalAudio"></a>

## PlayerLocalAudio Objects

```python
class PlayerLocalAudio()
```

Decode-and-output player backend. See module docstring for the state machine.


<a id="jukebox.player.backends.local_audio.PlayerLocalAudio.rewind"></a>

#### rewind

```python
def rewind()
```

Re-start current playlist from the first track.


<a id="jukebox.player.backends.local_audio.PlayerLocalAudio.replay"></a>

#### replay

```python
def replay()
```

Re-start playing the last-played folder.


<a id="jukebox.player.backends"></a>

# jukebox.player.backends

Playback backend implementations used by the player coordinator.


