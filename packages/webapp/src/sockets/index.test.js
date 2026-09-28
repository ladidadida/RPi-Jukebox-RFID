import { initSockets } from './index';
import {
  afterEach,
  beforeEach,
  describe,
  expect,
  test,
  vi,
} from 'vitest';

class FakeWebSocket {
  static instances = [];

  constructor(url) {
    this.url = url;
    this.readyState = 0;
    this.sent = [];
    FakeWebSocket.instances.push(this);
  }

  open() {
    this.readyState = 1;
    this.onopen();
  }

  message(message) {
    this.onmessage({ data: JSON.stringify(message) });
  }

  send(message) {
    this.sent.push(JSON.parse(message));
  }

  close() {
    this.readyState = 3;
    if (this.onclose) {
      this.onclose();
    }
  }
}

describe('initSockets', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    FakeWebSocket.instances = [];
    global.WebSocket = FakeWebSocket;
  });

  afterEach(() => {
    vi.useRealTimers();
    delete global.WebSocket;
  });

  test('subscribes, decodes events, and applies revocations', () => {
    let state = {};
    const setState = updater => {
      state = updater(state);
    };
    const cleanup = initSockets({
      events: ['player'],
      setState,
    });
    const socket = FakeWebSocket.instances[0];

    expect(socket.url).toBe('ws://localhost/api/v1/events');
    socket.open();
    expect(socket.sent).toEqual([{
      type: 'subscribe',
      topics: ['player'],
    }]);

    socket.message({
      type: 'event',
      topic: 'player.status',
      data: false,
    });
    expect(state).toEqual({ 'player.status': false });

    socket.message({
      type: 'revoke',
      topic: 'player.status',
    });
    expect(state).toEqual({});

    cleanup();
    expect(socket.sent[1]).toEqual({
      type: 'unsubscribe',
      topics: ['player'],
    });
  });

  test('reconnects with exponential delay and resubscribes', () => {
    const cleanup = initSockets({
      events: ['core', 'volume'],
      setState: vi.fn(),
    });
    const first = FakeWebSocket.instances[0];
    first.open();
    first.close();

    vi.advanceTimersByTime(999);
    expect(FakeWebSocket.instances).toHaveLength(1);
    vi.advanceTimersByTime(1);
    expect(FakeWebSocket.instances).toHaveLength(2);

    const second = FakeWebSocket.instances[1];
    second.open();
    expect(second.sent).toEqual([{
      type: 'subscribe',
      topics: ['core', 'volume'],
    }]);

    cleanup();
  });
});
