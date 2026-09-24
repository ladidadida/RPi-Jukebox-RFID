const commands = {
  getSingleCoverArt: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'get_single_coverart',
  },
  getAlbumCoverArt: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'get_album_coverart',
  },
  directoryTreeOfAudiofolder: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'list_all_dirs',
  },
  albumList: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'list_albums',
  },
  librarySources: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'list_library_sources',
  },
  libraryItems: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'list_library_items',
  },
  songList: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'list_songs_by_artist_and_album',
  },
  getSongByUrl: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'get_song_by_url',
    argKeys: ['song_url', 'provider']
  },
  folderList: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'get_folder_content',
  },
  cardsList: {
    rest: { method: 'GET', path: '/api/v1/cards' },
  },
  registerCard: {
    rest: { method: 'POST', path: '/api/v1/cards' },
  },
  deleteCard: {
    rest: { method: 'DELETE', path: '/api/v1/cards' },
  },
  // Migrated to real REST endpoints (see api/fastapi_server.py, register_player_routes) -- the
  // first slice of replacing the generic (package, plugin, method) RPC addressing, per
  // documentation/developers/roadmap-core-architecture.md. `request()` in utils/request.js
  // dispatches on the presence of `rest` instead of `_package`/`plugin`/`method`.
  playerstatus: {
    rest: { method: 'GET', path: '/api/v1/player/status' },
  },

  // Player Actions
  play: {
    rest: { method: 'POST', path: '/api/v1/player/play' },
  },
  play_single: {
    rest: { method: 'POST', path: '/api/v1/player/song' },
    argKeys: ['song_url', 'provider']
  },
  play_folder: {
    rest: { method: 'POST', path: '/api/v1/player/folder' },
    argKeys: ['folder']
  },
  play_album: {
    _package: 'player',
    plugin: 'ctrl',
    method: 'play_album',
    argKeys: ['albumartist', 'album', 'content_uri', 'provider']
  },
  pause: {
    rest: { method: 'POST', path: '/api/v1/player/pause' },
  },
  prev_song: {
    rest: { method: 'POST', path: '/api/v1/player/prev' },
  },
  next_song: {
    rest: { method: 'POST', path: '/api/v1/player/next' },
  },
  toggle: {
    rest: { method: 'POST', path: '/api/v1/player/toggle' },
  },
  shuffle: {
    rest: { method: 'POST', path: '/api/v1/player/shuffle' },
    argKeys: ['option'],
  },
  repeat: {
    rest: { method: 'POST', path: '/api/v1/player/repeat' },
    argKeys: ['option'],
  },
  seek: {
    // Renamed kwarg new_time -> position to match the REST body; only caller is seekbar.jsx.
    rest: { method: 'POST', path: '/api/v1/player/seek' },
    argKeys: ['position'],
  },

  // Volume
  setVolume: {
    // Was _package: 'volume' -- that namespace doesn't exist server-side at all (removed with
    // the old plugin system, never reintroduced), so this was a dead call. Now points at
    // player.ctrl's own volume methods, which do exist and always did.
    rest: { method: 'PUT', path: '/api/v1/player/volume' },
    argKeys: ['volume'],
  },
  getVolume: {
    rest: { method: 'GET', path: '/api/v1/player/volume' },
  },
  getMaxVolume: {
    _package: 'volume',
    plugin: 'ctrl',
    method: 'get_soft_max_volume',
  },
  setMaxVolume: {
    _package: 'volume',
    plugin: 'ctrl',
    method: 'set_soft_max_volume',
  },
  change_volume: {
    _package: 'volume',
    plugin: 'ctrl',
    method: 'change_volume',
    argKeys: ['step'],
  },
  toggleMuteVolume: {
    _package: 'volume',
    plugin: 'ctrl',
    method: 'mute',
  },
  getAudioOutputs: {
    _package: 'volume',
    plugin: 'ctrl',
    method: 'get_outputs',
  },
  setAudioOutput: {
    _package: 'volume',
    plugin: 'ctrl',
    method: 'set_output',
    argKeys: ['sink_index'],
  },
  toggle_output: {
    _package: 'volume',
    plugin: 'ctrl',
    method: 'toggle_output',
  },

  // Timers
  'timer_fade_volume.cancel': {
    _package: 'timers',
    plugin: 'timer_fade_volume',
    method: 'cancel',
  },
  'timer_fade_volume.get_state': {
    _package: 'timers',
    plugin: 'timer_fade_volume',
    method: 'get_state',
  },
  'timer_fade_volume': {
    _package: 'timers',
    plugin: 'timer_fade_volume',
    method: 'start',
    argKeys: ['wait_seconds', 'restart'],
    argDefaults: { restart: true },
  },
  'timer_shutdown.cancel': {
    _package: 'timers',
    plugin: 'timer_shutdown',
    method: 'cancel',
  },
  'timer_shutdown.get_state': {
    _package: 'timers',
    plugin: 'timer_shutdown',
    method: 'get_state',
  },
  'timer_shutdown': {
    _package: 'timers',
    plugin: 'timer_shutdown',
    method: 'start',
    argKeys: ['wait_seconds', 'restart'],
    argDefaults: { restart: true },
  },
  'timer_stop_player.cancel': {
    _package: 'timers',
    plugin: 'timer_stop_player',
    method: 'cancel',
  },
  'timer_stop_player.get_state': {
    _package: 'timers',
    plugin: 'timer_stop_player',
    method: 'get_state',
  },
  'timer_stop_player': {
    _package: 'timers',
    plugin: 'timer_stop_player',
    method: 'start',
    argKeys: ['wait_seconds', 'restart'],
    argDefaults: { restart: true },
  },


  'timer_idle_shutdown.cancel': {
    _package: 'timers',
    plugin: 'timer_idle_shutdown',
    method: 'cancel',
  },
  'timer_idle_shutdown.get_state': {
    _package: 'timers',
    plugin: 'timer_idle_shutdown',
    method: 'get_state',
  },
  'timer_idle_shutdown': {
    _package: 'timers',
    plugin: 'timer_idle_shutdown',
    method: 'start',
    argKeys: ['wait_seconds', 'restart'],
    argDefaults: { restart: true },
  },



  // Host
  getAutohotspotStatus: {
    _package: 'host',
    plugin: 'get_autohotspot_status',
  },
  startAutohotspot: {
    _package: 'host',
    plugin: 'start_autohotspot',
  },
  stopAutohotspot: {
    _package: 'host',
    plugin: 'stop_autohotspot',
  },
  getIpAddress: {
    _package: 'host',
    plugin: 'get_ip_address',
  },
  getDiskUsage: {
    _package: 'host',
    plugin: 'get_disk_usage',
  },
  reboot: {
    _package: 'host',
    plugin: 'reboot',
  },
  shutdown: {
    _package: 'host',
    plugin: 'shutdown',
  },
  say_my_ip: {
    _package: 'host',
    plugin: 'say_my_ip',
    argKeys: ['option'],
  },

  // Misc
  getAppSettings: {
    rest: { method: 'GET', path: '/api/v1/settings' },
  },

  setAppSettings: {
    rest: { method: 'PUT', path: '/api/v1/settings' },
    argKeys: ['settings'],
  },

  // Synchronisation
  'sync_rfidcards_all': {
    _package: 'sync_rfidcards',
    plugin: 'ctrl',
    method: 'sync_all'
  },
  'sync_rfidcards_change_on_rfid_scan': {
    _package: 'sync_rfidcards',
    plugin: 'ctrl',
    method: 'sync_change_on_rfid_scan',
    argKeys: ['option']
  },
};

export default commands;
