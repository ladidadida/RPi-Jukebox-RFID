import { createContext } from 'react';

const PlayerContext = createContext({
  isPlaying: false,
  requestInFlight: false,
});

export default PlayerContext;
