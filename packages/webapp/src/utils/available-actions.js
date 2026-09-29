import { useEffect, useState } from 'react';

import request from './request';

// Card actions offered by the running core modules and enabled plugins, fetched once per page load.
let pending = null;

const fetchAvailableActions = () => {
  if (pending === null) {
    pending = request('listActions').then(({ result }) => new Set((result || []).map(({ id }) => id)));
  }
  return pending;
};

const useAvailableActions = () => {
  const [actions, setActions] = useState(new Set());

  useEffect(() => {
    let active = true;
    fetchAvailableActions().then(available => {
      if (active) setActions(available);
    });
    return () => {
      active = false;
    };
  }, []);

  return actions;
};

export {
  fetchAvailableActions,
  useAvailableActions,
};
