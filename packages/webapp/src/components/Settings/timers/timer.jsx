import {
  useCallback,
  useContext,
  useEffect,
  useState,
} from 'react';
import { useTranslation } from 'react-i18next';
import { Box, ListItem, ListItemText, Typography } from '@mui/material';

import { Countdown } from '../../general';
import PubSubContext from '../../../context/pubsub/context';
import SetTimerDialog from './set-timer-dialog';
import request from '../../../utils/request';
import { TIMERS_TOPIC } from '../../../config';

// Timer state from the backend: the initial list entry, then every `timers.changed` event of this timer.
const useTimer = (initialState) => {
  const { name } = initialState;
  const { state: publisherState = {} } = useContext(PubSubContext);
  const published = publisherState[TIMERS_TOPIC];
  const [status, setStatus] = useState(initialState);
  const [revision, setRevision] = useState(0);
  const [error, setError] = useState(null);
  const [waitSeconds, setWaitSeconds] = useState(0);

  const apply = useCallback((timerState) => {
    setStatus(timerState);
    setRevision(value => value + 1);
    setError(null);
  }, []);

  useEffect(() => {
    if (published?.name === name) {
      apply(published);
    }
  }, [apply, name, published]);

  const cancelTimer = async () => {
    const { result, error: requestError } = await request('cancelTimer', { timer: name });
    if (requestError) {
      setError(requestError);
      return;
    }
    apply(result);
  };

  const setTimer = async (wait_seconds) => {
    if (wait_seconds <= 0) {
      return;
    }
    const { result, error: requestError } = await request('startTimer', { timer: name, wait_seconds });
    if (requestError) {
      setError(requestError);
      return;
    }
    apply(result);
  };

  return {
    status,
    enabled: status.enabled,
    revision,
    error,
    waitSeconds,
    setWaitSeconds,
    setTimer,
    cancelTimer,
  };
};

const TimerActions = ({ enabled, status, revision, error, type, onSetTimer, onCancelTimer, waitSeconds,
  onSetWaitSeconds }) => {
  const { t } = useTranslation();

  return (
    <Box sx={{ alignItems: 'center', display: 'flex', flexShrink: 0 }}>
      {enabled && (
        <Countdown
          seconds={status.remaining_seconds}
          resetKey={revision}
          stringEnded={t('settings.timers.ended')}
        />
      )}
      {error && <Typography>⚠️</Typography>}
      <SetTimerDialog
        type={type}
        enabled={enabled}
        setTimer={onSetTimer}
        cancelTimer={onCancelTimer}
        waitSeconds={waitSeconds}
        setWaitSeconds={onSetWaitSeconds}
      />
    </Box>
  );
};

const Timer = ({ timer }) => {
  const { t } = useTranslation();
  const state = useTimer(timer);
  const type = timer.name.replace(/_/g, '-');

  return (
    <ListItem
      disableGutters
      sx={{ alignItems: 'center', gap: 2 }}
    >
      <ListItemText
        primary={t(`settings.timers.${type}.title`, { defaultValue: timer.name })}
        secondary={t(`settings.timers.${type}.label`, { defaultValue: timer.action })}
        sx={{ minWidth: 0 }}
      />
      <TimerActions
        {...state}
        onSetTimer={state.setTimer}
        onCancelTimer={state.cancelTimer}
        onSetWaitSeconds={state.setWaitSeconds}
        type={type}
      />
    </ListItem>
  );
};

export default Timer;

export {
  TimerActions,
  useTimer,
};
