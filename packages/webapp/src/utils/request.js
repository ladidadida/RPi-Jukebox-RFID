import { socketRequest } from "../sockets";
import commands from "../commands";

// GET requests carry kwargs as query params (repeated for array values, matching FastAPI's
// convention for List[...] Query params); undefined/null values are omitted rather than sent
// as the literal string 'undefined'/'null'.
const toQueryString = (kwargs) => {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(kwargs)) {
    if (value === undefined || value === null) {
      continue;
    }
    if (Array.isArray(value)) {
      value.forEach((entry) => params.append(key, entry));
    }
    else {
      params.append(key, value);
    }
  }
  return params.toString();
};

// Migrated commands carry a `rest: {method, path}` definition instead of the RPC
// `_package`/`plugin`/`method` shape (see commands/index.js) -- this is the one place that
// needs to know about it, so the ~10 call sites across the app keep calling
// request('someCommand', kwargs) exactly as before regardless of which transport backs it.
const restRequest = async ({ method, path }, kwargs) => {
  const options = { method };
  let requestPath = path;
  if (method === 'GET') {
    const query = toQueryString(kwargs);
    if (query) {
      requestPath = `${path}?${query}`;
    }
  }
  else {
    options.headers = { 'Content-Type': 'application/json' };
    options.body = JSON.stringify(kwargs);
  }

  const response = await fetch(requestPath, options);
  if (!response.ok) {
    const body = await response.text().catch(() => '');
    throw new Error(`Request failed with HTTP ${response.status}${body ? `: ${body}` : ''}`);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
};

const request = async (command, kwargs = {}) => {
  try {
    if (!(command in commands)) {
      throw new Error(`'${command}' does not exist in command object`);
    }

    const definition = commands[command];
    const result = definition.rest
      ? await restRequest(definition.rest, kwargs)
      : await socketRequest(definition._package, definition.plugin, definition.method ?? null, kwargs);
    return { result };
  }
  catch (error) {
    console.error(`${command}: `, error);
    return { error };
  };
};

export default request;
