const commands = {
  getSingleCoverArt: {
    rest: { method: 'GET', path: '/api/v1/library/cover/song' },
  },
  getAlbumCoverArt: {
    rest: { method: 'GET', path: '/api/v1/library/cover/album' },
  },
  librarySources: {
    rest: { method: 'GET', path: '/api/v1/library/sources' },
  },
  libraryItems: {
    rest: { method: 'GET', path: '/api/v1/library/items' },
  },
  songList: {
    rest: { method: 'GET', path: '/api/v1/library/songs' },
  },
  getSongByUrl: {
    rest: { method: 'GET', path: '/api/v1/library/song' },
    argKeys: ['song_url', 'provider']
  },
  cardsList: {
    rest: { method: 'GET', path: '/api/v1/cards' },
  },
  registerCard: {
    rest: { method: 'POST', path: '/api/v1/cards' },
  },
  deleteCard: {
    rest: { method: 'DELETE', path: '/api/v1/cards/{card_id}' },
  },
  playerstatus: {
    rest: { method: 'GET', path: '/api/v1/player/status' },
  },

  // Player Actions
  play: {
    rest: { method: 'POST', path: '/api/v1/player/play' },
    cardAction: 'player.play',
  },
  play_single: {
    rest: { method: 'POST', path: '/api/v1/player/song' },
    cardAction: 'player.play_single',
    argKeys: ['song_url', 'provider']
  },
  play_folder: {
    rest: { method: 'POST', path: '/api/v1/player/folder' },
    cardAction: 'player.play_folder',
    argKeys: ['folder']
  },
  play_album: {
    rest: { method: 'POST', path: '/api/v1/player/album' },
    cardAction: 'player.play_album',
    argKeys: ['albumartist', 'album', 'content_uri', 'provider']
  },
  pause: {
    rest: { method: 'POST', path: '/api/v1/player/pause' },
    cardAction: 'player.pause',
  },
  prev_song: {
    rest: { method: 'POST', path: '/api/v1/player/prev' },
    cardAction: 'player.prev',
  },
  next_song: {
    rest: { method: 'POST', path: '/api/v1/player/next' },
    cardAction: 'player.next',
  },
  toggle: {
    rest: { method: 'POST', path: '/api/v1/player/toggle' },
    cardAction: 'player.toggle',
  },
  shuffle: {
    rest: { method: 'POST', path: '/api/v1/player/shuffle' },
    cardAction: 'player.shuffle',
    argKeys: ['option'],
  },
  repeat: {
    rest: { method: 'POST', path: '/api/v1/player/repeat' },
    cardAction: 'player.repeat',
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

  // Removed: getMaxVolume/setMaxVolume/change_volume/toggleMuteVolume/getAudioOutputs/
  // setAudioOutput/toggle_output (volume.ctrl), the whole timers.* family, getAutohotspotStatus/
  // startAutohotspot/stopAutohotspot/getIpAddress/getDiskUsage/reboot/shutdown/say_my_ip (host),
  // and sync_rfidcards_all/sync_rfidcards_change_on_rfid_scan (sync_rfidcards.ctrl) -- all
  // addressed RPC packages that don't exist server-side (removed with the old plugin system,
  // never reintroduced). Coming back once those are reintroduced as components/plugins.

  // Misc
  getAppSettings: {
    rest: { method: 'GET', path: '/api/v1/settings' },
  },

  setAppSettings: {
    rest: { method: 'PUT', path: '/api/v1/settings' },
    argKeys: ['settings'],
  },
};

export default commands;
