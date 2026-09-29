import { useEffect, useState } from 'react';

import PlayerContext from './context';
import { initSockets } from '../../sockets';
import { PLAYER_STATUS_TOPIC } from '../../config';

const PlayerProvider = ({ children }) => {
  const [state, setState] = useState({});

  // Initialize sockets for player context
  useEffect(() => (
    initSockets({
      events: [PLAYER_STATUS_TOPIC],
      setState,
    })
  ), []);

  const context = {
    setState,
    state,
  };

  // Should be called <PlayerFunctions.Provider />
  // and `state` should be moved to PlayerStatus.Provider

  return(
      <PlayerContext.Provider value={context}>
        { children }
      </PlayerContext.Provider>
    )
};

export default PlayerProvider;
