import { act, renderHook } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';

import PubSubContext from '../../../context/pubsub/context';
import request from '../../../utils/request';
import { useTimer } from './timer';

vi.mock('../../../utils/request', () => ({
  default: vi.fn(),
}));

const initial = {
  name: 'stop_player',
  action: 'player.stop',
  available: true,
  enabled: false,
  remaining_seconds: 0,
  wait_seconds: 3600,
};

const renderTimer = (state) => {
  const wrapper = ({ children }) => (
    <PubSubContext.Provider value={{ state: state.current, setState: vi.fn() }}>
      {children}
    </PubSubContext.Provider>
  );
  return renderHook(() => useTimer(initial), { wrapper });
};

afterEach(() => {
  vi.clearAllMocks();
});

test('only events of its own timer change the state', () => {
  const state = { current: {} };
  const { result, rerender } = renderTimer(state);
  expect(result.current.enabled).toBe(false);

  state.current = { 'timers.changed': { ...initial, name: 'fade_volume', enabled: true } };
  rerender();
  expect(result.current.enabled).toBe(false);

  state.current = { 'timers.changed': { ...initial, enabled: true, remaining_seconds: 60 } };
  rerender();
  expect(result.current.enabled).toBe(true);
  expect(result.current.status.remaining_seconds).toBe(60);
});

test('start and cancel send the timer name', async () => {
  request.mockResolvedValueOnce({ result: { ...initial, enabled: true, remaining_seconds: 300 } });
  const { result } = renderTimer({ current: {} });

  await act(() => result.current.setTimer(300));
  expect(request).toHaveBeenCalledWith('startTimer', { timer: 'stop_player', wait_seconds: 300 });
  expect(result.current.enabled).toBe(true);

  request.mockResolvedValueOnce({ result: initial });
  await act(() => result.current.cancelTimer());
  expect(request).toHaveBeenCalledWith('cancelTimer', { timer: 'stop_player' });
  expect(result.current.enabled).toBe(false);
});
