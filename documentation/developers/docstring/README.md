# None

## Table of Contents

* [jukebox](#jukebox)
* [jukebox.library](#jukebox.library)
  * [LibraryError](#jukebox.library.LibraryError)
  * [resolve\_library\_path](#jukebox.library.resolve_library_path)
  * [UploadSession](#jukebox.library.UploadSession)
  * [MusicLibrary](#jukebox.library.MusicLibrary)
  * [create\_music\_library](#jukebox.library.create_music_library)
* [jukebox.utils](#jukebox.utils)
  * [decode\_rpc\_call](#jukebox.utils.decode_rpc_call)
  * [decode\_rpc\_command](#jukebox.utils.decode_rpc_command)
  * [decode\_and\_call\_rpc\_command](#jukebox.utils.decode_and_call_rpc_command)
  * [bind\_rpc\_command](#jukebox.utils.bind_rpc_command)
  * [rpc\_call\_to\_str](#jukebox.utils.rpc_call_to_str)
  * [get\_config\_action](#jukebox.utils.get_config_action)
  * [generate\_cmd\_alias\_rst](#jukebox.utils.generate_cmd_alias_rst)
  * [generate\_cmd\_alias\_reference](#jukebox.utils.generate_cmd_alias_reference)
  * [get\_git\_state](#jukebox.utils.get_git_state)
* [jukebox.command\_aliases](#jukebox.command_aliases)
* [jukebox.rfid.reader](#jukebox.rfid.reader)
  * [RfidCardDetectCallbacks](#jukebox.rfid.reader.RfidCardDetectCallbacks)
    * [register](#jukebox.rfid.reader.RfidCardDetectCallbacks.register)
    * [run\_callbacks](#jukebox.rfid.reader.RfidCardDetectCallbacks.run_callbacks)
  * [rfid\_card\_detect\_callbacks](#jukebox.rfid.reader.rfid_card_detect_callbacks)
  * [CardRemovalTimerClass](#jukebox.rfid.reader.CardRemovalTimerClass)
    * [\_\_init\_\_](#jukebox.rfid.reader.CardRemovalTimerClass.__init__)
  * [start\_readers](#jukebox.rfid.reader.start_readers)
* [jukebox.rfid.configure](#jukebox.rfid.configure)
  * [reader\_install\_dependencies](#jukebox.rfid.configure.reader_install_dependencies)
  * [reader\_load\_module](#jukebox.rfid.configure.reader_load_module)
  * [query\_user\_for\_reader](#jukebox.rfid.configure.query_user_for_reader)
  * [write\_config](#jukebox.rfid.configure.write_config)
* [jukebox.rfid.hardware.fake\_reader\_gui.gpioz\_gui\_addon](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon)
  * [create\_inputs](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.create_inputs)
  * [set\_state](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.set_state)
  * [que\_set\_state](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.que_set_state)
  * [fix\_state](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.fix_state)
  * [pbox\_set\_state](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.pbox_set_state)
  * [que\_set\_pbox](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.que_set_pbox)
  * [create\_outputs](#jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.create_outputs)
* [jukebox.rfid.hardware.fake\_reader\_gui.description](#jukebox.rfid.hardware.fake_reader_gui.description)
* [jukebox.rfid.hardware.fake\_reader\_gui.fake\_reader\_gui](#jukebox.rfid.hardware.fake_reader_gui.fake_reader_gui)
* [jukebox.rfid.hardware.rdm6300\_serial.rdm6300\_serial](#jukebox.rfid.hardware.rdm6300_serial.rdm6300_serial)
  * [decode](#jukebox.rfid.hardware.rdm6300_serial.rdm6300_serial.decode)
* [jukebox.rfid.hardware.rdm6300\_serial.description](#jukebox.rfid.hardware.rdm6300_serial.description)
* [jukebox.rfid.hardware.mfrc522\_i2c.mfrc522\_i2c](#jukebox.rfid.hardware.mfrc522_i2c.mfrc522_i2c)
* [jukebox.rfid.hardware.mfrc522\_i2c.description](#jukebox.rfid.hardware.mfrc522_i2c.description)
* [jukebox.rfid.hardware.rc522\_spi.rc522\_spi](#jukebox.rfid.hardware.rc522_spi.rc522_spi)
* [jukebox.rfid.hardware.rc522\_spi.description](#jukebox.rfid.hardware.rc522_spi.description)
* [jukebox.rfid.hardware.pn532\_i2c\_py532.pn532\_i2c\_py532](#jukebox.rfid.hardware.pn532_i2c_py532.pn532_i2c_py532)
* [jukebox.rfid.hardware.pn532\_i2c\_py532.description](#jukebox.rfid.hardware.pn532_i2c_py532.description)
* [jukebox.rfid.hardware.generic\_nfcpy.description](#jukebox.rfid.hardware.generic_nfcpy.description)
* [jukebox.rfid.hardware.generic\_nfcpy.generic\_nfcpy](#jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy)
  * [ReaderClass](#jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass)
    * [cleanup](#jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass.cleanup)
    * [stop](#jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass.stop)
    * [read\_card](#jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass.read_card)
* [jukebox.rfid.hardware.template\_new\_reader.template\_new\_reader](#jukebox.rfid.hardware.template_new_reader.template_new_reader)
  * [query\_customization](#jukebox.rfid.hardware.template_new_reader.template_new_reader.query_customization)
  * [ReaderClass](#jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass)
    * [\_\_init\_\_](#jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.__init__)
    * [cleanup](#jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.cleanup)
    * [stop](#jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.stop)
    * [read\_card](#jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.read_card)
* [jukebox.rfid.hardware.template\_new\_reader.description](#jukebox.rfid.hardware.template_new_reader.description)
* [jukebox.rfid.hardware.generic\_usb.generic\_usb](#jukebox.rfid.hardware.generic_usb.generic_usb)
* [jukebox.rfid.hardware.generic\_usb.description](#jukebox.rfid.hardware.generic_usb.description)
* [jukebox.rfid.readerbase](#jukebox.rfid.readerbase)
  * [ReaderBaseClass](#jukebox.rfid.readerbase.ReaderBaseClass)
* [jukebox.rfid](#jukebox.rfid)
* [jukebox.rfid.cards](#jukebox.rfid.cards)
  * [list\_cards](#jukebox.rfid.cards.list_cards)
  * [delete\_card](#jukebox.rfid.cards.delete_card)
  * [register\_card](#jukebox.rfid.cards.register_card)
  * [register\_card\_custom](#jukebox.rfid.cards.register_card_custom)
  * [save\_card\_database](#jukebox.rfid.cards.save_card_database)
  * [register](#jukebox.rfid.cards.register)
* [jukebox.rfid.cardutils](#jukebox.rfid.cardutils)
  * [decode\_card\_command](#jukebox.rfid.cardutils.decode_card_command)
  * [card\_command\_to\_str](#jukebox.rfid.cardutils.card_command_to_str)
  * [card\_to\_str](#jukebox.rfid.cardutils.card_to_str)
* [jukebox.nv\_manager](#jukebox.nv_manager)
* [jukebox.publishing.bus](#jukebox.publishing.bus)
  * [EventBus](#jukebox.publishing.bus.EventBus)
    * [publish](#jukebox.publishing.bus.EventBus.publish)
    * [resend](#jukebox.publishing.bus.EventBus.resend)
    * [cache\_snapshot](#jukebox.publishing.bus.EventBus.cache_snapshot)
* [jukebox.publishing](#jukebox.publishing)
  * [get\_bus](#jukebox.publishing.get_bus)
  * [Publisher](#jukebox.publishing.Publisher)
    * [send](#jukebox.publishing.Publisher.send)
    * [revoke](#jukebox.publishing.Publisher.revoke)
    * [resend](#jukebox.publishing.Publisher.resend)
    * [close\_server](#jukebox.publishing.Publisher.close_server)
  * [get\_publisher](#jukebox.publishing.get_publisher)
  * [republish](#jukebox.publishing.republish)
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
* [jukebox.api.dispatch](#jukebox.api.dispatch)
  * [process\_request](#jukebox.api.dispatch.process_request)
* [jukebox.api.fastapi\_server](#jukebox.api.fastapi_server)
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
  * [write\_yaml](#jukebox.cfghandler.write_yaml)
* [jukebox.callingback](#jukebox.callingback)
  * [CallbackHandler](#jukebox.callingback.CallbackHandler)
    * [register](#jukebox.callingback.CallbackHandler.register)
    * [run\_callbacks](#jukebox.callingback.CallbackHandler.run_callbacks)
    * [has\_callbacks](#jukebox.callingback.CallbackHandler.has_callbacks)
* [jukebox.registry](#jukebox.registry)
  * [register](#jukebox.registry.register)
  * [callable\_method](#jukebox.registry.callable_method)
  * [call](#jukebox.registry.call)
  * [call\_ignore\_errors](#jukebox.registry.call_ignore_errors)
  * [dump\_registry](#jukebox.registry.dump_registry)
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
* [jukebox.daemon](#jukebox.daemon)
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
* [jukebox.system](#jukebox.system)
  * [get\_start\_time](#jukebox.system.get_start_time)
  * [get\_log](#jukebox.system.get_log)
  * [get\_log\_debug](#jukebox.system.get_log_debug)
  * [get\_log\_error](#jukebox.system.get_log_error)
  * [get\_git\_state](#jukebox.system.get_git_state)
  * [empty\_rpc\_call](#jukebox.system.empty_rpc_call)
  * [get\_app\_settings](#jukebox.system.get_app_settings)
  * [set\_app\_settings](#jukebox.system.set_app_settings)
* [jukebox.player.mpd\_plugin](#jukebox.player.mpd_plugin)
  * [initialize\_mpd\_player](#jukebox.player.mpd_plugin.initialize_mpd_player)
* [jukebox.player.coordinator](#jukebox.player.coordinator)
  * [PlayerCoordinator](#jukebox.player.coordinator.PlayerCoordinator)
    * [register\_backend](#jukebox.player.coordinator.PlayerCoordinator.register_backend)
    * [select\_backend](#jukebox.player.coordinator.PlayerCoordinator.select_backend)
* [jukebox.player.playcontentcallback](#jukebox.player.playcontentcallback)
  * [PlayContentCallbacks](#jukebox.player.playcontentcallback.PlayContentCallbacks)
    * [register](#jukebox.player.playcontentcallback.PlayContentCallbacks.register)
    * [run\_callbacks](#jukebox.player.playcontentcallback.PlayContentCallbacks.run_callbacks)
* [jukebox.player.plugin](#jukebox.player.plugin)
* [jukebox.player](#jukebox.player)
  * [play\_card\_callbacks](#jukebox.player.play_card_callbacks)
  * [MusicLibPath](#jukebox.player.MusicLibPath)
  * [get\_music\_library\_path](#jukebox.player.get_music_library_path)
* [jukebox.player.backends.coverart\_cache\_manager](#jukebox.player.backends.coverart_cache_manager)
* [jukebox.player.backends.mpd](#jukebox.player.backends.mpd)
  * [PlayerMPD](#jukebox.player.backends.mpd.PlayerMPD)
    * [mpd\_retry\_with\_mutex](#jukebox.player.backends.mpd.PlayerMPD.mpd_retry_with_mutex)
    * [pause](#jukebox.player.backends.mpd.PlayerMPD.pause)
    * [next](#jukebox.player.backends.mpd.PlayerMPD.next)
    * [rewind](#jukebox.player.backends.mpd.PlayerMPD.rewind)
    * [replay](#jukebox.player.backends.mpd.PlayerMPD.replay)
    * [toggle](#jukebox.player.backends.mpd.PlayerMPD.toggle)
    * [replay\_if\_stopped](#jukebox.player.backends.mpd.PlayerMPD.replay_if_stopped)
    * [is\_second\_swipe](#jukebox.player.backends.mpd.PlayerMPD.is_second_swipe)
    * [play\_second\_swipe](#jukebox.player.backends.mpd.PlayerMPD.play_second_swipe)
    * [flush\_coverart\_cache](#jukebox.player.backends.mpd.PlayerMPD.flush_coverart_cache)
    * [get\_folder\_content](#jukebox.player.backends.mpd.PlayerMPD.get_folder_content)
    * [play\_folder](#jukebox.player.backends.mpd.PlayerMPD.play_folder)
    * [play\_album](#jukebox.player.backends.mpd.PlayerMPD.play_album)
    * [get\_volume](#jukebox.player.backends.mpd.PlayerMPD.get_volume)
    * [set\_volume](#jukebox.player.backends.mpd.PlayerMPD.set_volume)
* [jukebox.player.backends](#jukebox.player.backends)

<a id="jukebox"></a>

# jukebox

<a id="jukebox.library"></a>

# jukebox.library

Safe file operations within the configured MPD music library.


<a id="jukebox.library.LibraryError"></a>

## LibraryError Objects

```python
class LibraryError(Exception)
```

An expected library operation failure suitable for an HTTP response.


<a id="jukebox.library.resolve_library_path"></a>

#### resolve\_library\_path

```python
def resolve_library_path(root,
                         value,
                         *,
                         allow_root=True,
                         require_exists=False)
```

Resolve a relative or internal absolute path without escaping ``root``.


<a id="jukebox.library.UploadSession"></a>

## UploadSession Objects

```python
class UploadSession()
```

Write one upload to a temporary file and publish it atomically.


<a id="jukebox.library.MusicLibrary"></a>

## MusicLibrary Objects

```python
class MusicLibrary()
```

Perform validated mutations beneath a lazily resolved library root.


<a id="jukebox.library.create_music_library"></a>

#### create\_music\_library

```python
def create_music_library()
```

Create the production library service after the player component is started.


<a id="jukebox.utils"></a>

# jukebox.utils

Common utility functions


<a id="jukebox.utils.decode_rpc_call"></a>

#### decode\_rpc\_call

```python
def decode_rpc_call(cfg_rpc_call: Dict) -> Optional[Dict]
```

Makes sure that the core rpc call parameters have valid default values in cfg_rpc_call.

> [!IMPORTANT]
> Leaves all other parameters in cfg_action untouched or later downstream processing!

**Arguments**:

- `cfg_rpc_call`: RPC command as configuration entry

**Returns**:

A fully populated deep copy of cfg_rpc_call

<a id="jukebox.utils.decode_rpc_command"></a>

#### decode\_rpc\_command

```python
def decode_rpc_command(cfg_rpc_cmd: Dict,
                       logger: logging.Logger = log) -> Optional[Dict]
```

Decode an RPC Command from a config entry.

This means

* Decode RPC command alias (if present)
* Ensure all RPC call parameters have valid default values

If the command alias cannot be decoded correctly, the command is mapped to misc.empty_rpc_call
which emits a misuse warning when called
If an explicitly specified this is not done. However, it is ensured that the returned
dictionary contains all mandatory parameters for an RPC call. RPC call functions have error handling
for non-existing RPC commands and we get a clearer error message.

**Arguments**:

- `cfg_rpc_cmd`: RPC command as configuration entry
- `logger`: The logger to use

**Returns**:

A decoded, fully populated deep copy of cfg_rpc_cmd

<a id="jukebox.utils.decode_and_call_rpc_command"></a>

#### decode\_and\_call\_rpc\_command

```python
def decode_and_call_rpc_command(rpc_cmd: Dict, logger: logging.Logger = log)
```

Convenience function combining decode_rpc_command and plugs.call_ignore_errors


<a id="jukebox.utils.bind_rpc_command"></a>

#### bind\_rpc\_command

```python
def bind_rpc_command(cfg_rpc_cmd: Dict,
                     dereference=False,
                     logger: logging.Logger = log)
```

Decode an RPC command configuration entry and bind it to a function

**Arguments**:

- `dereference`: Dereference even the call to plugs.call(...)
    ``. If false, the returned function is ``plugs.call(package, plugin, method, *args, **kwargs)`` with
        all checks applied at bind time
    ``. If true, the returned function is ``package.plugin.method(*args, **kwargs)`` with
        all checks applied at bind time.

Setting deference to True, circumvents the dynamic nature of the plugins: the function to call
    must exist at bind time and cannot change. If False, the function to call must only exist at call time.
    This can be important during the initialization where package ordering and initialization means that not all
    classes have been instantiated yet. With dereference=True also the plugs thread lock for serialization of calls
    is circumvented. Use with care!

**Returns**:

Callable function w/o parameters which directly runs the RPC command
using plugs.call_ignore_errors

<a id="jukebox.utils.rpc_call_to_str"></a>

#### rpc\_call\_to\_str

```python
def rpc_call_to_str(cfg_rpc_call: Dict, with_args=True) -> str
```

Return a readable string of an RPC call config

**Arguments**:

- `cfg_rpc_call`: RPC call configuration entry
- `with_args`: Return string shall include the arguments of the function

<a id="jukebox.utils.get_config_action"></a>

#### get\_config\_action

```python
def get_config_action(cfg, section, option, default, valid_actions_dict,
                      logger)
```

Looks up the given {section}.{option} config option and returns

the associated entry from valid_actions_dict, if valid. Falls back to the given
default otherwise.


<a id="jukebox.utils.generate_cmd_alias_rst"></a>

#### generate\_cmd\_alias\_rst

```python
def generate_cmd_alias_rst(stream)
```

Write a reference of all rpc command aliases in Restructured Text format


<a id="jukebox.utils.generate_cmd_alias_reference"></a>

#### generate\_cmd\_alias\_reference

```python
def generate_cmd_alias_reference(stream)
```

Write a reference of all rpc command aliases in text format


<a id="jukebox.utils.get_git_state"></a>

#### get\_git\_state

```python
def get_git_state()
```

Return git state information for the current branch


<a id="jukebox.command_aliases"></a>

# jukebox.command\_aliases

This file provides definitions for RPC command aliases

See [RPC Commands](../../builders/rpc-commands.md)

Trimmed to the components that survived the plugin-system removal (see
documentation/developers/roadmap-core-architecture.md): only 'player' right now. Aliases for
volume/host/timers/synchronisation will come back once those are reintroduced as components.


<a id="jukebox.rfid.reader"></a>

# jukebox.rfid.reader

<a id="jukebox.rfid.reader.RfidCardDetectCallbacks"></a>

## RfidCardDetectCallbacks Objects

```python
class RfidCardDetectCallbacks(CallbackHandler)
```

Callbacks are executed if rfid card is detected


<a id="jukebox.rfid.reader.RfidCardDetectCallbacks.register"></a>

#### register

```python
def register(func: Callable[[str, RfidCardDetectState], None])
```

Add a new callback function :attr:`func`.

Callback signature is

.. py:function:: func(card_id: str, state: int)
    :noindex:

**Arguments**:

- `card_id`: Card ID
- `state`: See `RfidCardDetectState`

<a id="jukebox.rfid.reader.RfidCardDetectCallbacks.run_callbacks"></a>

#### run\_callbacks

```python
def run_callbacks(card_id: str, state: RfidCardDetectState)
```



<a id="jukebox.rfid.reader.rfid_card_detect_callbacks"></a>

#### rfid\_card\_detect\_callbacks

Callback handler instance for rfid_card_detect_callbacks events.

See [`RfidCardDetectCallbacks`](#jukebox.rfid.reader.RfidCardDetectCallbacks)


<a id="jukebox.rfid.reader.CardRemovalTimerClass"></a>

## CardRemovalTimerClass Objects

```python
class CardRemovalTimerClass(threading.Thread)
```

A timer watchdog thread that calls timeout_action on time-out


<a id="jukebox.rfid.reader.CardRemovalTimerClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__(on_timeout_callback, logger: logging.Logger = None)
```

**Arguments**:

- `on_timeout_callback`: The function to execute on time-out

<a id="jukebox.rfid.reader.start_readers"></a>

#### start\_readers

```python
def start_readers()
```

Load the reader config/database and start a ReaderRunner thread per configured reader.

Called explicitly by jukebox.daemon at start-up (no plugin system, see
documentation/developers/roadmap-core-architecture.md).


<a id="jukebox.rfid.configure"></a>

# jukebox.rfid.configure

<a id="jukebox.rfid.configure.reader_install_dependencies"></a>

#### reader\_install\_dependencies

```python
def reader_install_dependencies(reader_path: str,
                                dependency_install: str) -> None
```

Install dependencies for the selected reader module

**Arguments**:

- `reader_path`: Path to the reader module
- `dependency_install`: how to handle installing of dependencies
'query': query user (default)
'auto': automatically
'no': don't install dependencies

<a id="jukebox.rfid.configure.reader_load_module"></a>

#### reader\_load\_module

```python
def reader_load_module(reader_name)
```

Load the module for the reader_name

A ModuleNotFoundError is unrecoverable, but we at least want to give some hint how to resolve that to the user
All other errors will NOT be handled. Modules that do not load due to compile errors have other problems

**Arguments**:

- `reader_name`: Name of the reader to load the module for

**Returns**:

module

<a id="jukebox.rfid.configure.query_user_for_reader"></a>

#### query\_user\_for\_reader

```python
def query_user_for_reader(dependency_install='query') -> dict
```

Ask the user to select a RFID reader and prompt for the reader's configuration

This function performs the following steps, to find and present all available readers to the user

- search for available reader subpackages
- dynamically load the description module for each reader subpackage
- queries user for selection
- if no_dep_install=False, install dependencies as given by requirements.txt and execute setup.inc.sh of subpackage
- dynamically load the actual reader module from the reader subpackage
- if selected reader has customization options query user for that now
- return configuration

There are checks to make sure we have the right reader modules and they are what we expect.
The are as few requirements towards the reader module as possible and everything else is optional
(see reader_template for these requirements)
However, there is no error handling w.r.t to user input and reader's query_config. Firstly, in this script
we cannot gracefully handle an exception that occurs on reader level, and secondly the exception will simply
exit the script w/o writing the config to file. No harm done.

This script expects to reside in the directory with all the reader subpackages, i.e it is part of the rfid-reader package.
Otherwise you'll need to adjust sys.path

**Arguments**:

- `dependency_install`: how to handle installing of dependencies
'query': query user (default)
'auto': automatically
'no': don't install dependencies

**Returns**:

`dict as {section: {parameter: value}}`: nested dict with entire configuration that can be read into ConfigParser

<a id="jukebox.rfid.configure.write_config"></a>

#### write\_config

```python
def write_config(config_file: str,
                 config_dict: dict,
                 force_overwrite=False) -> None
```

Write configuration to config_file

**Arguments**:

- `config_file`: relative or absolute path to config file
- `config_dict`: nested dict with configuration parameters for ConfigParser consumption
- `force_overwrite`: overwrite existing configuration file without asking

<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon"></a>

# jukebox.rfid.hardware.fake\_reader\_gui.gpioz\_gui\_addon

Add GPIO input devices and output devices to the RFID Mock Reader GUI


<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.create_inputs"></a>

#### create\_inputs

```python
def create_inputs(frame, default_btn_width, default_padx, default_pady)
```

Add all input devies to the GUI

**Arguments**:

- `frame`: The TK frame (e.g. LabelFrame) in the main GUI to add the buttons to

**Returns**:

List of all added GUI buttons

<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.set_state"></a>

#### set\_state

```python
def set_state(value, box_state_var)
```

Change the value of a checkbox state variable


<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.que_set_state"></a>

#### que\_set\_state

```python
def que_set_state(value, box_state_var)
```

Queue the action to change a checkbox state variable to the TK GUI main thread


<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.fix_state"></a>

#### fix\_state

```python
def fix_state(box_state_var)
```

Prevent a checkbox state variable to change on checkbox mouse press


<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.pbox_set_state"></a>

#### pbox\_set\_state

```python
def pbox_set_state(value, pbox_state_var, label_var)
```

Update progress bar state and related state label


<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.que_set_pbox"></a>

#### que\_set\_pbox

```python
def que_set_pbox(value, pbox_state_var, label_var)
```

Queue the action to change the progress bar state to the TK GUI main thread


<a id="jukebox.rfid.hardware.fake_reader_gui.gpioz_gui_addon.create_outputs"></a>

#### create\_outputs

```python
def create_outputs(frame, default_btn_width, default_padx, default_pady)
```

Add all output devices to the GUI

**Arguments**:

- `frame`: The TK frame (e.g. LabelFrame) in the main GUI to add the representations to

**Returns**:

List of all added GUI objects

<a id="jukebox.rfid.hardware.fake_reader_gui.description"></a>

# jukebox.rfid.hardware.fake\_reader\_gui.description

<a id="jukebox.rfid.hardware.fake_reader_gui.fake_reader_gui"></a>

# jukebox.rfid.hardware.fake\_reader\_gui.fake\_reader\_gui

<a id="jukebox.rfid.hardware.rdm6300_serial.rdm6300_serial"></a>

# jukebox.rfid.hardware.rdm6300\_serial.rdm6300\_serial

<a id="jukebox.rfid.hardware.rdm6300_serial.rdm6300_serial.decode"></a>

#### decode

```python
def decode(raw_card_id: bytearray, number_format: int) -> str
```

Decode the RDM6300 data format into actual card ID


<a id="jukebox.rfid.hardware.rdm6300_serial.description"></a>

# jukebox.rfid.hardware.rdm6300\_serial.description

<a id="jukebox.rfid.hardware.mfrc522_i2c.mfrc522_i2c"></a>

# jukebox.rfid.hardware.mfrc522\_i2c.mfrc522\_i2c

<a id="jukebox.rfid.hardware.mfrc522_i2c.description"></a>

# jukebox.rfid.hardware.mfrc522\_i2c.description

<a id="jukebox.rfid.hardware.rc522_spi.rc522_spi"></a>

# jukebox.rfid.hardware.rc522\_spi.rc522\_spi

<a id="jukebox.rfid.hardware.rc522_spi.description"></a>

# jukebox.rfid.hardware.rc522\_spi.description

<a id="jukebox.rfid.hardware.pn532_i2c_py532.pn532_i2c_py532"></a>

# jukebox.rfid.hardware.pn532\_i2c\_py532.pn532\_i2c\_py532

<a id="jukebox.rfid.hardware.pn532_i2c_py532.description"></a>

# jukebox.rfid.hardware.pn532\_i2c\_py532.description

<a id="jukebox.rfid.hardware.generic_nfcpy.description"></a>

# jukebox.rfid.hardware.generic\_nfcpy.description

List of supported devices https://nfcpy.readthedocs.io/en/latest/overview.html


<a id="jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy"></a>

# jukebox.rfid.hardware.generic\_nfcpy.generic\_nfcpy

<a id="jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass"></a>

## ReaderClass Objects

```python
class ReaderClass(ReaderBaseClass)
```

The reader class for nfcpy supported NFC card readers.


<a id="jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass.cleanup"></a>

#### cleanup

```python
def cleanup()
```

The cleanup function: free and release all resources used by this card reader (if any).


<a id="jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass.stop"></a>

#### stop

```python
def stop()
```

This function is called to tell the reader to exit its reading function.


<a id="jukebox.rfid.hardware.generic_nfcpy.generic_nfcpy.ReaderClass.read_card"></a>

#### read\_card

```python
def read_card() -> str
```

Blocking or non-blocking function that waits for a new card to appear and return the card's UID as string


<a id="jukebox.rfid.hardware.template_new_reader.template_new_reader"></a>

# jukebox.rfid.hardware.template\_new\_reader.template\_new\_reader

<a id="jukebox.rfid.hardware.template_new_reader.template_new_reader.query_customization"></a>

#### query\_customization

```python
def query_customization() -> dict
```

Query the user for reader parameter customization

This function will be called during the configuration/setup phase when the user selects this reader module.
It must return all configuration parameters that are necessary to later use the Reader class.
You can ask the user for selections and choices. And/or provide default values.
If your reader requires absolutely no configuration return {}


<a id="jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass"></a>

## ReaderClass Objects

```python
class ReaderClass(ReaderBaseClass)
```

The actual reader class that is used to read RFID cards.

It will be instantiated once and then read_card() is called in an endless loop.

It will be used in a  manner
  with Reader(reader_cfg_key) as reader:
    for card_id in reader:
      ...
which ensures proper resource de-allocation. For this to work derive this class from ReaderBaseClass.
All the required interfaces are implemented there.

Put your code into these functions (see below for more information)
  - `__init__`
  - read_card
  - cleanup
  - stop


<a id="jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__(reader_cfg_key)
```

In the constructor, you will get the `reader_cfg_key` with which you can access the configuration data

As you are dealing directly with potentially user-manipulated config information, it is
advisable to do some sanity checks and give useful error messages. Even if you cannot recover gracefully,
a good error message helps :-)


<a id="jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.cleanup"></a>

#### cleanup

```python
def cleanup()
```

The cleanup function: free and release all resources used by this card reader (if any).

Put all your cleanup code here, e.g. if you are using the serial bus or GPIO pins.
Will be called implicitly via the __exit__ function
This function must exist! If there is nothing to do, just leave the pass statement in place below


<a id="jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.stop"></a>

#### stop

```python
def stop()
```

This function is called to tell the reader to exist it's reading function.

This function is called before cleanup is called.

> [!NOTE]
> This is usually called from a different thread than the reader's thread! And this is the reason for the
> two-step exit strategy. This function works across threads to indicate to the reader that is should stop attempt
> to read a card. Once called, the function read_card will not be called again. When the reader thread exits
> cleanup is called from the reader thread itself.


<a id="jukebox.rfid.hardware.template_new_reader.template_new_reader.ReaderClass.read_card"></a>

#### read\_card

```python
def read_card() -> str
```

Blocking or non-blocking function that waits for a new card to appear and return the card's UID as string

This is were your main code goes :-)
This function must return a string with the card id
In case of error, it may return None or an empty string

The function should break and return with an empty string, once stop() is called


<a id="jukebox.rfid.hardware.template_new_reader.description"></a>

# jukebox.rfid.hardware.template\_new\_reader.description

Provide a short title for this reader.

This is what that user will see when asked for selecting his RFID reader
So, be precise but readable. Precise means 40 characters or less


<a id="jukebox.rfid.hardware.generic_usb.generic_usb"></a>

# jukebox.rfid.hardware.generic\_usb.generic\_usb

<a id="jukebox.rfid.hardware.generic_usb.description"></a>

# jukebox.rfid.hardware.generic\_usb.description

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

Handling the RFID card database

A few considerations:
- Changing the Card DB influences to current state
  - rfid.reader: Does not care, as it always freshly looks into the DB when a new card is triggered
  - fake_reader_gui: Initializes the Drop-down menu once on start --> Will get out of date!

Do we need a notifier? Or a callback for modules to get notified?
Do we want to publish the information about a card DB update?
TODO: Add callback for on_database_change

TODO: check card id type (if int, convert to str)
TODO: check if args is really a list (convert if not?)


<a id="jukebox.rfid.cards.list_cards"></a>

#### list\_cards

```python
def list_cards()
```

Provide a summarized, decoded list of all card actions

This is intended as basis for a formatter function

Format: 'id': {decoded_function_call, ignore_same_id_delay, ignore_card_removal_action, description, from_alias}


<a id="jukebox.rfid.cards.delete_card"></a>

#### delete\_card

```python
def delete_card(card_id: str, auto_save: bool = True)
```

**Arguments**:

- `auto_save`: 
- `card_id`: 

<a id="jukebox.rfid.cards.register_card"></a>

#### register\_card

```python
def register_card(card_id: str,
                  cmd_alias: str,
                  args: Optional[List] = None,
                  kwargs: Optional[Dict] = None,
                  ignore_card_removal_action: Optional[bool] = None,
                  ignore_same_id_delay: Optional[bool] = None,
                  overwrite: bool = False,
                  auto_save: bool = True)
```

Register a new card based on quick-selection

If you are going to call this through the RPC it will get a little verbose

**Example:** Registering a new card with ID *0009* for increment volume with a custom argument to inc_volume
(*here: 15*) and custom *ignore_same_id_delay value*::

    plugin.call_ignore_errors('cards', 'register_card',
                              args=['0009', 'inc_volume'],
                              kwargs={'args': [15], 'ignore_same_id_delay': True, 'overwrite': True})


<a id="jukebox.rfid.cards.register_card_custom"></a>

#### register\_card\_custom

```python
def register_card_custom()
```

Register a new card with full RPC call specification (Not implemented yet)


<a id="jukebox.rfid.cards.save_card_database"></a>

#### save\_card\_database

```python
def save_card_database(filename=None, *, only_if_changed=True)
```

Store the current card database. If filename is None, it is saved back to the file it was loaded from


<a id="jukebox.rfid.cards.register"></a>

#### register

```python
def register()
```

Register the card-database RPC calls as 'cards.<name>'.

Called explicitly by jukebox.daemon at start-up (no plugin system, see
documentation/developers/roadmap-core-architecture.md).


<a id="jukebox.rfid.cardutils"></a>

# jukebox.rfid.cardutils

Common card decoding functions

TODO: Thread safety when accessing the card DB!


<a id="jukebox.rfid.cardutils.decode_card_command"></a>

#### decode\_card\_command

```python
def decode_card_command(cfg_rpc_cmd: Mapping, logger: logging.Logger = log)
```

Extension of utils.decode_action with card-specific parameters


<a id="jukebox.rfid.cardutils.card_command_to_str"></a>

#### card\_command\_to\_str

```python
def card_command_to_str(cfg_rpc_cmd: Mapping, long=False) -> List[str]
```

Returns a list of strings with [card_action, ignore_same_id_delay, ignore_card_removal_action]

The last two parameters are only present, if *long* is True and if they are present in the cfg_rpc_cmd


<a id="jukebox.rfid.cardutils.card_to_str"></a>

#### card\_to\_str

```python
def card_to_str(card_id: str, long=False) -> List[str]
```

Returns a list of strings from card entry command in the format of :func:`card_command_to_str`


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

<a id="jukebox.publishing.get_bus"></a>

#### get\_bus

```python
def get_bus() -> EventBus
```

The shared, thread-safe event bus. Prefer get_publisher() for the send/resend API.


<a id="jukebox.publishing.Publisher"></a>

## Publisher Objects

```python
class Publisher()
```

Thin, source-compatible wrapper around the shared :class:`EventBus`.

Kept as a class only so existing call sites (``publishing.get_publisher().send(...)``) don't
need to change. Unlike the old ZMQ-backed Publisher, a single shared instance is safe to use
from any thread -- the "one Publisher per thread" rule from the ZMQ days is gone along with
ZMQ (see documentation/developers/roadmap-core-architecture.md).


<a id="jukebox.publishing.Publisher.send"></a>

#### send

```python
def send(topic: str, payload) -> None
```

Send out a message for topic


<a id="jukebox.publishing.Publisher.revoke"></a>

#### revoke

```python
def revoke(topic: str) -> None
```

Revoke a single topic element (not a topic tree!)


<a id="jukebox.publishing.Publisher.resend"></a>

#### resend

```python
def resend(topic: Optional[str] = None) -> None
```

Re-send current status of the topic tree `topic` (default: everything) to all subscribers.

Not necessary to call after incremental updates or new subscriptions -- that happens
automatically.


<a id="jukebox.publishing.Publisher.close_server"></a>

#### close\_server

```python
def close_server() -> None
```

No-op, kept for source compatibility with the old shutdown call.

There is no separate server thread to close down anymore -- the bus is just an object.


<a id="jukebox.publishing.get_publisher"></a>

#### get\_publisher

```python
def get_publisher() -> Publisher
```

Return the shared publisher instance.

Example::

    import jukebox.publishing as publishing
    publishing.get_publisher().send('hello', f'Hi there, howya?')


<a id="jukebox.publishing.republish"></a>

#### republish

```python
def republish(topic=None)
```

Re-publish the topic tree 'topic' to all subscribers

**Arguments**:

- `topic`: Topic tree to republish. None = resend all

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


<a id="jukebox.api.dispatch"></a>

# jukebox.api.dispatch

Transport-neutral processing for Jukebox RPC requests.


<a id="jukebox.api.dispatch.process_request"></a>

#### process\_request

```python
def process_request(client_request, received_at_ns=None)
```

Execute an RPC request and return its response envelope.

The request is copied before any values are passed to plugin code so the
caller's dictionary, including nested ``args`` and ``kwargs``, is retained.


<a id="jukebox.api.fastapi_server"></a>

# jukebox.api.fastapi\_server

FastAPI + uvicorn HTTP and WebSocket API server.

The sole browser-facing HTTP/WebSocket bridge -- replaced the Tornado-based `jukebox.api.server`
(see documentation/developers/roadmap-core-architecture.md, steps 2-6). Serves health, RPC
passthrough, events-over-websocket, the library upload/folder/entries/refresh endpoints, and (see
jukebox.api.webapp_static) the webapp's static build + /logs -- nginx is gone, this is now the one
thing reachable from the LAN, hence `api.bind_address` defaulting to 0.0.0.0.

The RPC executor here is sized for concurrency rather than serialized to one worker like the Tornado
version was: unlike the old `jukebox.plugs` system this replaced, `jukebox.registry.call()` has no
shared global lock, so multiple executor workers actually buy real concurrency now -- each component
is responsible for its own thread-safety.


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

<a id="jukebox.callingback"></a>

# jukebox.callingback

Provides a generic callback handler


<a id="jukebox.callingback.CallbackHandler"></a>

## CallbackHandler Objects

```python
class CallbackHandler()
```

Generic Callback Handler to collect callbacks functions through :func:`register` and execute them

with :func:`run_callbacks`

A lock is used to sequence registering of new functions and running callbacks.

**Arguments**:

- `name`: A name of this handler for usage in log messages
- `logger`: The logger instance to use for logging
- `context`: A custom context handler to use as lock. If none, a local :class:`threading.Lock()` will be created

<a id="jukebox.callingback.CallbackHandler.register"></a>

#### register

```python
def register(func: Optional[Callable[..., None]])
```

Register a new function to be executed when the callback event happens

**Arguments**:

- `func`: The function to register. If set to :data:`None`, this register request is silently ignored.

<a id="jukebox.callingback.CallbackHandler.run_callbacks"></a>

#### run\_callbacks

```python
def run_callbacks(*args, **kwargs)
```

Run all registered callbacks.

*ALL* exceptions from callback functions will be caught and logged only.
Exceptions are not raised upwards!


<a id="jukebox.callingback.CallbackHandler.has_callbacks"></a>

#### has\_callbacks

```python
@property
def has_callbacks()
```



<a id="jukebox.registry"></a>

# jukebox.registry

Explicit call registry for core components.

Replaces the old dynamic, config-driven plugin system (formerly ``jukebox.plugs``): components are
registered directly by ``daemon.py`` at start-up instead of being discovered from ``jukebox.yaml`` via
decorator magic (``@plugs.register`` / ``@plugs.initialize`` / ``@plugs.finalize`` / ``@plugs.atexit``).

There is no dynamic loading and no module-wide serializing lock here (the old ``plugs.py`` serialized
every call through one global lock regardless of which component it targeted -- see
documentation/developers/roadmap-core-architecture.md). Each component is responsible for its own
thread-safety.

Call addressing (``package``, ``plugin``, ``method``) is unchanged from the old system so the webapp's
RPC call shape (``{'package': ..., 'plugin': ..., 'method': ...}``) keeps working without changes on
that side.


<a id="jukebox.registry.register"></a>

#### register

```python
def register(obj: Any, name: str, package: str) -> Any
```

Register ``obj`` (a function, bound method, or class instance) under ``package.name``.


<a id="jukebox.registry.callable_method"></a>

#### callable\_method

```python
def callable_method(func: Callable) -> Callable
```

Mark a bound method as callable through the registry (i.e. over RPC).


<a id="jukebox.registry.call"></a>

#### call

```python
def call(package: str,
         plugin: str,
         method: Optional[str] = None,
         *,
         args=(),
         kwargs=None,
         as_thread: bool = False,
         thread_name: Optional[str] = None) -> Any
```

Call a registered function/method. See the old ``jukebox.plugs.call`` for the historical

behavioural contract this preserves (addressing, ``as_thread`` semantics).


<a id="jukebox.registry.call_ignore_errors"></a>

#### call\_ignore\_errors

```python
def call_ignore_errors(package: str,
                       plugin: str,
                       method: Optional[str] = None,
                       *,
                       args=(),
                       kwargs=None,
                       as_thread: bool = False,
                       thread_name: Optional[str] = None) -> Any
```

Like :func:`call`, but exceptions are logged and swallowed rather than propagated.


<a id="jukebox.registry.dump_registry"></a>

#### dump\_registry

```python
def dump_registry(stream)
```

Write a human readable summary of all registered callables to stream.


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

A race-safe, single-execution timer with plugin/RPC support.


<a id="jukebox.multitimer.GenericTimerClass.start"></a>

#### start

```python
@plugin.tag
def start(wait_seconds: Optional[float] = None, restart: bool = True)
```

Start the timer, atomically replacing an active generation by default.


<a id="jukebox.multitimer.GenericTimerClass.cancel"></a>

#### cancel

```python
@plugin.tag
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
@plugin.tag
def toggle()
```

Toggle between active and disabled states.


<a id="jukebox.multitimer.GenericTimerClass.trigger"></a>

#### trigger

```python
@plugin.tag
def trigger()
```

Trigger the active generation immediately.


<a id="jukebox.multitimer.GenericTimerClass.is_alive"></a>

#### is\_alive

```python
@plugin.tag
def is_alive() -> bool
```

Return whether a timer generation is logically active.


<a id="jukebox.multitimer.GenericTimerClass.get_timeout"></a>

#### get\_timeout

```python
@plugin.tag
def get_timeout() -> float
```

Return the configured timeout in seconds.


<a id="jukebox.multitimer.GenericTimerClass.set_timeout"></a>

#### set\_timeout

```python
@plugin.tag
def set_timeout(wait_seconds: float) -> float
```

Set the timeout, atomically replacing an active generation.


<a id="jukebox.multitimer.GenericTimerClass.publish"></a>

#### publish

```python
@plugin.tag
def publish()
```

Publish the current timer state.


<a id="jukebox.multitimer.GenericTimerClass.get_state"></a>

#### get\_state

```python
@plugin.tag
def get_state() -> Dict[str, Any]
```

Return the RPC-compatible timer state.


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
@plugin.tag
def get_state() -> Dict[str, Any]
```

Return the RPC-compatible periodic timer state.


<a id="jukebox.daemon"></a>

# jukebox.daemon

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


<a id="jukebox.system"></a>

# jukebox.system

Miscellaneous RPC calls, registered explicitly by jukebox.daemon (no plugin system)


<a id="jukebox.system.get_start_time"></a>

#### get\_start\_time

```python
def get_start_time()
```

Time when JukeBox has been started


<a id="jukebox.system.get_log"></a>

#### get\_log

```python
def get_log(handler_name: str)
```

Get the log file from the loggers (debug_file_handler, error_file_handler)


<a id="jukebox.system.get_log_debug"></a>

#### get\_log\_debug

```python
def get_log_debug()
```

Get the log file (from the debug_file_handler)


<a id="jukebox.system.get_log_error"></a>

#### get\_log\_error

```python
def get_log_error()
```

Get the log file (from the error_file_handler)


<a id="jukebox.system.get_git_state"></a>

#### get\_git\_state

```python
def get_git_state()
```

Return git state information for the current branch


<a id="jukebox.system.empty_rpc_call"></a>

#### empty\_rpc\_call

```python
def empty_rpc_call(msg: str = '')
```

This function does nothing.

The RPC command alias 'none' is mapped to this function.

This is also used when configuration errors lead to non existing RPC command alias definitions.
When the alias definition is void, we still want to return a valid function to simplify error handling
up the module call stack.

**Arguments**:

- `msg`: If present, this message is send to the logger with severity warning

<a id="jukebox.system.get_app_settings"></a>

#### get\_app\_settings

```python
def get_app_settings()
```

Return settings for web app stored in jukebox.yaml


<a id="jukebox.system.set_app_settings"></a>

#### set\_app\_settings

```python
def set_app_settings(settings={})
```

Set configuration settings for the web app.


<a id="jukebox.player.mpd_plugin"></a>

# jukebox.player.mpd\_plugin

<a id="jukebox.player.mpd_plugin.initialize_mpd_player"></a>

#### initialize\_mpd\_player

```python
def initialize_mpd_player() -> PlayerCoordinator
```

Create the coordinator with MPD as its sole backend and register it as 'player.ctrl'.


<a id="jukebox.player.coordinator"></a>

# jukebox.player.coordinator

<a id="jukebox.player.coordinator.PlayerCoordinator"></a>

## PlayerCoordinator Objects

```python
class PlayerCoordinator()
```

Provider-neutral facade for playback and content backends.


<a id="jukebox.player.coordinator.PlayerCoordinator.register_backend"></a>

#### register\_backend

```python
def register_backend(name: str,
                     backend: Any,
                     make_active: bool = False) -> None
```

Register a backend, selecting the first registered backend by default.


<a id="jukebox.player.coordinator.PlayerCoordinator.select_backend"></a>

#### select\_backend

```python
@plugs.tag
def select_backend(name: str)
```

Stop the current backend and select another registered backend.


<a id="jukebox.player.playcontentcallback"></a>

# jukebox.player.playcontentcallback

<a id="jukebox.player.playcontentcallback.PlayContentCallbacks"></a>

## PlayContentCallbacks Objects

```python
class PlayContentCallbacks(Generic[STATE], CallbackHandler)
```

Callbacks executed before card-triggered playback actions.


<a id="jukebox.player.playcontentcallback.PlayContentCallbacks.register"></a>

#### register

```python
def register(func: Callable[[str, STATE], None])
```

Register a callback with the signature ``callback(content, state)``.

**Arguments**:

- `func`: Callback to register

<a id="jukebox.player.playcontentcallback.PlayContentCallbacks.run_callbacks"></a>

#### run\_callbacks

```python
def run_callbacks(content: str, state: STATE)
```



<a id="jukebox.player.plugin"></a>

# jukebox.player.plugin

Player start-up/shutdown, called explicitly by jukebox.daemon (no plugin system).


<a id="jukebox.player"></a>

# jukebox.player

<a id="jukebox.player.play_card_callbacks"></a>

#### play\_card\_callbacks

Callback handler for card-triggered playback. This belongs to the player

facade rather than to a specific playback backend.


<a id="jukebox.player.MusicLibPath"></a>

## MusicLibPath Objects

```python
class MusicLibPath()
```

Extract the music directory from the mpd.conf file


<a id="jukebox.player.get_music_library_path"></a>

#### get\_music\_library\_path

```python
def get_music_library_path()
```

Get the music library path


<a id="jukebox.player.backends.coverart_cache_manager"></a>

# jukebox.player.backends.coverart\_cache\_manager

Cover-art cache support for the MPD backend.


<a id="jukebox.player.backends.mpd"></a>

# jukebox.player.backends.mpd

Package for interfacing with the MPD Music Player Daemon

Status information in three topics
1) Player Status: published only on change
  This is a subset of the MPD status (and not the full MPD status) ??
  - folder
  - song
  - volume (volume is published only via player status, and not separatly to avoid too many Threads)
  - ...
2) Elapsed time: published every 250 ms, unless constant
  - elapsed
3) Folder Config: published only on change
   This belongs to the folder being played
   Publish:
   - random, resume, single, loop
   On save store this information:
   Contains the information for resume functionality of each folder
   - random, resume, single, loop
   - if resume:
     - current song, elapsed
   - what is PLAYSTATUS for?
   When to save
   - on stop
   Angstsave:
   - on pause (only if box get turned off without proper shutdown - else stop gets implicitly called)
   - on status change of random, resume, single, loop (for resume omit current status if currently playing- this has now meaning)
   Load checks:
   - if resume, but no song, elapsed -> log error and start from the beginning

Status storing:
  - Folder config for each folder (see above)
  - Information to restart last folder playback, which is:
    - last_folder -> folder_on_close
    - song, elapsed
    - random, resume, single, loop
    - if resume is enabled, after start we need to set last_played_folder, such that card swipe is detected as second swipe?!
      on the other hand: if resume is enabled, this is also saved to folder.config -> and that is checked by play card

Internal status
  - last played folder: Needed to detect second swipe


Saving {'player_status': {'last_played_folder': 'TraumfaengerStarkeLieder', 'CURRENTSONGPOS': '0', 'CURRENTFILENAME': 'TraumfaengerStarkeLieder/01.mp3'},
'audio_folder_status':
{'TraumfaengerStarkeLieder': {'ELAPSED': '1.0', 'CURRENTFILENAME': 'TraumfaengerStarkeLieder/01.mp3', 'CURRENTSONGPOS': '0', 'PLAYSTATUS': 'stop', 'RESUME': 'OFF', 'SHUFFLE': 'OFF', 'LOOP': 'OFF', 'SINGLE': 'OFF'},
'Giraffenaffen': {'ELAPSED': '1.0', 'CURRENTFILENAME': 'TraumfaengerStarkeLieder/01.mp3', 'CURRENTSONGPOS': '0', 'PLAYSTATUS': 'play', 'RESUME': 'OFF', 'SHUFFLE': 'OFF', 'LOOP': 'OFF', 'SINGLE': 'OFF'}}}

References:
https://github.com/Mic92/python-mpd2
https://python-mpd2.readthedocs.io/en/latest/topics/commands.html
https://mpd.readthedocs.io/en/latest/protocol.html

sudo -u mpd speaker-test -t wav -c 2


<a id="jukebox.player.backends.mpd.PlayerMPD"></a>

## PlayerMPD Objects

```python
class PlayerMPD()
```

Interface to MPD Music Player Daemon


<a id="jukebox.player.backends.mpd.PlayerMPD.mpd_retry_with_mutex"></a>

#### mpd\_retry\_with\_mutex

```python
def mpd_retry_with_mutex(mpd_cmd, *args)
```

This method adds thread saftey for acceses to mpd via a mutex lock,

it shall be used for each access to mpd to ensure thread safety
In case of a communication error the connection will be reestablished and the pending command will be repeated 2 times

I think this should be refactored to a decorator


<a id="jukebox.player.backends.mpd.PlayerMPD.pause"></a>

#### pause

```python
@plugs.tag
def pause(state: int = 1)
```

Enforce pause to state (1: pause, 0: resume)

This is what you want as card removal action: pause the playback, so it can be resumed when card is placed
on the reader again. What happens on re-placement depends on configured second swipe option


<a id="jukebox.player.backends.mpd.PlayerMPD.next"></a>

#### next

```python
@plugs.tag
def next()
```

Play next track in current playlist


<a id="jukebox.player.backends.mpd.PlayerMPD.rewind"></a>

#### rewind

```python
@plugs.tag
def rewind()
```

Re-start current playlist from first track

Note: Will not re-read folder config, but leave settings untouched


<a id="jukebox.player.backends.mpd.PlayerMPD.replay"></a>

#### replay

```python
@plugs.tag
def replay()
```

Re-start playing the last-played folder

Will reset settings to folder config


<a id="jukebox.player.backends.mpd.PlayerMPD.toggle"></a>

#### toggle

```python
@plugs.tag
def toggle()
```

Toggle pause state, i.e. do a pause / resume depending on current state


<a id="jukebox.player.backends.mpd.PlayerMPD.replay_if_stopped"></a>

#### replay\_if\_stopped

```python
@plugs.tag
def replay_if_stopped()
```

Re-start playing the last-played folder unless playlist is still playing

> [!NOTE]
> To me this seems much like the behaviour of play,
> but we keep it as it is specifically implemented in box 2.X


<a id="jukebox.player.backends.mpd.PlayerMPD.is_second_swipe"></a>

#### is\_second\_swipe

```python
def is_second_swipe(folder: str) -> bool
```

Return whether a card request should run the configured second-swipe action.


<a id="jukebox.player.backends.mpd.PlayerMPD.play_second_swipe"></a>

#### play\_second\_swipe

```python
def play_second_swipe()
```

Run the configured second-swipe action.


<a id="jukebox.player.backends.mpd.PlayerMPD.flush_coverart_cache"></a>

#### flush\_coverart\_cache

```python
@plugs.tag
def flush_coverart_cache()
```

Deletes the Cover Art Cache


<a id="jukebox.player.backends.mpd.PlayerMPD.get_folder_content"></a>

#### get\_folder\_content

```python
@plugs.tag
def get_folder_content(folder: str)
```

Get the folder content as content list with meta-information. Depth is always 1.

Call repeatedly to descend in hierarchy

**Arguments**:

- `folder`: Folder path relative to music library path

<a id="jukebox.player.backends.mpd.PlayerMPD.play_folder"></a>

#### play\_folder

```python
@plugs.tag
def play_folder(folder: str, recursive: bool = False) -> None
```

Playback a music folder.

Folder content is added to the playlist as described by :mod:`jukebox.playlistgenerator`.
The playlist is cleared first.

**Arguments**:

- `folder`: Folder path relative to music library path
- `recursive`: Add folder recursively

<a id="jukebox.player.backends.mpd.PlayerMPD.play_album"></a>

#### play\_album

```python
@plugs.tag
def play_album(albumartist: str, album: str)
```

Playback a album found in MPD database.

All album songs are added to the playlist
The playlist is cleared first.

**Arguments**:

- `albumartist`: Artist of the Album provided by MPD database
- `album`: Album name provided by MPD database

<a id="jukebox.player.backends.mpd.PlayerMPD.get_volume"></a>

#### get\_volume

```python
def get_volume()
```

Get the current volume

For volume control do not use directly, but use through the plugin 'volume',
as the user may have configured a volume control manager other than MPD


<a id="jukebox.player.backends.mpd.PlayerMPD.set_volume"></a>

#### set\_volume

```python
def set_volume(volume)
```

Set the volume

For volume control do not use directly, but use through the plugin 'volume',
as the user may have configured a volume control manager other than MPD


<a id="jukebox.player.backends"></a>

# jukebox.player.backends

Playback backend implementations used by the player coordinator.


