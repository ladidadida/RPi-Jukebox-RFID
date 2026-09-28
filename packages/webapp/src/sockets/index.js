import { PUBSUB_ENDPOINT } from '../config';
import {
  decodePubSubMessage,
  encodeMessage,
} from './utils';

const RECONNECT_MIN_MS = 1000;
const RECONNECT_MAX_MS = 30000;

let eventSocket = null;
let reconnectTimer = null;
let reconnectDelay = RECONNECT_MIN_MS;
const eventListeners = new Set();

const currentTopics = () => (
  new Set(
    Array.from(eventListeners)
      .flatMap(({ events }) => events)
  )
);

const sendSubscription = (type, topics) => {
  if (eventSocket === null || eventSocket.readyState !== 1 || topics.length === 0) {
    return;
  }
  eventSocket.send(encodeMessage({ type, topics }));
};

const eventSocketUrl = () => {
  const url = new URL(PUBSUB_ENDPOINT, window.location.href);
  url.protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return url.toString();
};

const dispatchEvent = (message) => {
  const { type, topic, data, error } = decodePubSubMessage(message);
  if (error) {
    console.error(`[Events]: ${error}`);
    return;
  }

  eventListeners.forEach(({ setState, events }) => {
    if (!events.some(subscription => topic.startsWith(subscription))) {
      return;
    }

    if (type === 'revoke') {
      setState(state => {
        const nextState = { ...state };
        delete nextState[topic];
        return nextState;
      });
    }
    else {
      setState(state => ({ ...state, [topic]: data }));
    }
  });
};

function scheduleReconnect() {
  if (reconnectTimer !== null || eventListeners.size === 0) {
    return;
  }
  reconnectTimer = setTimeout(() => {
    reconnectTimer = null;
    connectEventSocket();
  }, reconnectDelay);
  reconnectDelay = Math.min(reconnectDelay * 2, RECONNECT_MAX_MS);
}

function connectEventSocket() {
  if (
    eventListeners.size === 0 ||
    (eventSocket !== null && [0, 1].includes(eventSocket.readyState))
  ) {
    return;
  }

  const socket = new WebSocket(eventSocketUrl());
  eventSocket = socket;

  socket.onopen = () => {
    if (eventSocket !== socket) {
      return;
    }
    reconnectDelay = RECONNECT_MIN_MS;
    sendSubscription('subscribe', Array.from(currentTopics()));
  };

  socket.onmessage = ({ data }) => {
    if (eventSocket === socket) {
      dispatchEvent(data);
    }
  };

  socket.onerror = () => {
    if (eventSocket === socket && socket.readyState < 2) {
      socket.close();
    }
  };

  socket.onclose = () => {
    if (eventSocket !== socket) {
      return;
    }
    eventSocket = null;
    scheduleReconnect();
  };
}

const initSockets = ({ setState, events = [] }) => {
  const previousTopics = currentTopics();
  const listener = { setState, events: [...events] };
  eventListeners.add(listener);
  const addedTopics = events.filter(topic => !previousTopics.has(topic));

  connectEventSocket();
  sendSubscription('subscribe', addedTopics);

  return () => {
    eventListeners.delete(listener);
    const remainingTopics = currentTopics();
    const removedTopics = events.filter(topic => !remainingTopics.has(topic));
    sendSubscription('unsubscribe', removedTopics);

    if (eventListeners.size === 0) {
      if (reconnectTimer !== null) {
        clearTimeout(reconnectTimer);
        reconnectTimer = null;
      }
      if (eventSocket !== null) {
        const socket = eventSocket;
        eventSocket = null;
        socket.close();
      }
    }
  };
};

export {
  initSockets,
};
