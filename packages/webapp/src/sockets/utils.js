const encodeMessage = (obj) => {
  return JSON.stringify(obj);
}

const decodePubSubMessage = (message) => {
  try {
    const decoded = (typeof message === 'string') ?
      JSON.parse(message) :
      message;
    const {
      type,
      topic,
      data = undefined,
    } = decoded;

    if (!['event', 'revoke'].includes(type) || typeof topic !== 'string') {
      throw new Error('Invalid event message.');
    }
    return { type, topic, data };
  }
  catch (error) {
    return { error };
  }
}

export {
  decodePubSubMessage,
  encodeMessage,
}
