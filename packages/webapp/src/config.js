const PUBSUB_ENDPOINT = '/api/v1/events';

const PLAYER_STATUS_TOPIC = 'player.status';
const CARD_DETECTED_TOPIC = 'rfid.card_detected';
const SYSTEM_INFO_TOPIC = 'system.info';

const SUBSCRIPTIONS = [
  'batt_status',
  'host.timer.cputemp',
  'host.temperature.cpu',
  CARD_DETECTED_TOPIC,
  SYSTEM_INFO_TOPIC,
];

const ROOT_DIR = './';

// TODO: The reason why thos commands are empty objects is due to a legacy
// situation where titles associated with those commands were stored here
// After the intro of i18n, those titles became obsolete. Because changing
// the data structure from object to array requires some refactoring, this
// was not done yet to maintain functionality. It's ok to change the command
// object keys to arrays, but some downstream methods need to change as well
const JUKEBOX_ACTIONS_MAP = {
  // Command Aliases
  // Player
  play_music: {
    commands: {
      play_album: {},
      play_folder: {},
      play_single: {},
    }
  },

  // Audio & Volume
  // Note: no volume control here -- change_volume/toggle_output need the removed pulse-output
  // component back (see roadmap-core-architecture.md, "Old plugin system removed"), not
  // currently a Jukebox capability.
  audio: {
    commands: {
      play: {},
      pause: {},
      toggle: {},
      next_song: {},
      prev_song: {},
      shuffle: {},
      repeat: {},
    },
  },

  // host/timers/synchronisation categories removed: they addressed the host/timers/
  // sync_rfidcards RPC packages, none of which exist server-side (removed with the old plugin
  // system, never reintroduced) -- restoring these needs those components back first.
}

const TIMER_STEPS = [0, 2, 5, 10, 15, 20, 30, 45, 60, 120, 180, 240];

export {
  CARD_DETECTED_TOPIC,
  JUKEBOX_ACTIONS_MAP,
  PLAYER_STATUS_TOPIC,
  PUBSUB_ENDPOINT,
  ROOT_DIR,
  SUBSCRIPTIONS,
  SYSTEM_INFO_TOPIC,
  TIMER_STEPS,
}
