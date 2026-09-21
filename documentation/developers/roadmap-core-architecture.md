# Roadmap: Core Architecture (Fork)

> Fork context: diverging from upstream because the direction they're pursuing isn't the direction we
> want. Building on `future3/develop` as a base — swap pieces incrementally, keep something runnable
> after every step, ditch what turns out to be dead weight along the way rather than carrying it forward.

Fork goals, roughly in the order we're tackling them:

1. **Core architecture** (this doc) — first, because everything else sits on top of it.
2. **Advanced plugin system** — being rethought from scratch, not adopted from upstream's
   `future3/draft-entrypoint-plugins` draft. Goal is *powerful* plugins, which likely means hooking
   deeper into the architecture than a config-toggled entry-point list — worth deciding once the core
   architecture (this doc) has taken shape, since what a plugin can hook into depends on what the
   core looks like. See "Relationship to the other tracks" below.
3. **Packaging/install overhaul** — install logic entirely in Python, one package + subpackages, CLI
   drives system setup instead of ~20 bash scripts. Upstream already scoped this in
   `documentation/developers/roadmap-plugins-and-packaging.md` (Track B) — largely reusable, not
   reinvented here.
4. **New name** — deferred, no dependency on the above.

## Current state (inherited from future3/develop)

- **Backend core**: ZMQ REP RPC server (`src/jukebox/jukebox/rpc/server.py`) — single-threaded blocking
  `recv()` loop, calls `jukebox.plugs.call()` synchronously per request. Also used inproc
  (`inproc://JukeBoxRpcServer`) so internal components (e.g. GPIO button handlers) call through the same
  path as external clients.
- **Browser-facing layer**: Tornado (`src/jukebox/jukebox/api/server.py`) bridges HTTP + WebSocket to
  that RPC. Already reasonably shaped — health check, RPC passthrough, library upload/CRUD, events over
  WebSocket via an `EventBroker` fed by ZMQ SUB — but:
  - RPC calls run through a `ThreadPoolExecutor(max_workers=1)`, which serializes all RPC traffic
    through the browser API. Same shape as the bottleneck diagnosed in a previous session (single
    REP socket + unbounded MPD timeout wedges all web requests) — just moved one layer up.
  - Library endpoints get their own executor, also sized 1.
  - No FastAPI/uvicorn anywhere yet — Tornado is the actual HTTP stack today.
- **CLI**: `run_rpc_tool.py` talks to the ZMQ REP server directly, bypassing Tornado entirely.
- **Plugin dispatch**: `jukebox.plugs.call(package, plugin, method, args, kwargs, as_thread=...)` —
  synchronous, with an opt-in "run in a separate thread" escape hatch used ad hoc per call site.

## Goal

FastAPI + uvicorn as the one middleware layer between browser (HTTP + WebSocket), CLI, and internal
plugin calls. Drop the ZMQ REP hop where it's pure indirection; decide separately whether ZMQ pub/sub is
still the right tool for the event/broadcast side once Tornado (which needed the `ZMQStream` bridge) is
gone.

## Why incremental, not big-bang

Agreed approach: build on `future3/develop`, swap parts one at a time, always have something that runs.
Expect to need cleanup passes between steps rather than one clean rewrite.

## Proposed steps

1. **Inventory concurrency needs first.** Which plugin calls are safe to run in parallel vs. must stay
   serialized against shared hardware state (audio playback, GPIO, MPD)? This decides whether "high
   performance" comes from more executor workers, from making `plugs.call` async-aware, or both — the
   real design question here, not just a mechanical framework swap.

   **Finding:** `jukebox.plugs.call()` already serializes *every* dispatched call behind one
   module-level `threading.RLock` (`_lock_module` in `src/jukebox/jukebox/plugs.py`), independent of
   which plugin/component is being called. So the `ThreadPoolExecutor(max_workers=1)` sizing in the
   Tornado bridge isn't the only serialization point — even with more HTTP-layer concurrency, all
   plugin calls still queue up behind this single lock today. Real parallelism (e.g. a library scan
   running while playback controls stay responsive) requires replacing this one-lock-for-everything
   model with something per-component/per-resource — not yet designed, tracked as an open decision
   below.
2. **Stand up FastAPI alongside Tornado**, reimplementing health/RPC/events first, still backed by the
   existing ZMQ REP client. Proves the swap without touching core dispatch.

   **Status: done.** `src/jukebox/jukebox/api/fastapi_server.py` (`FastApiServer`, `create_app`)
   reimplements health/RPC/events on FastAPI + uvicorn, running independently of and side by side with
   `jukebox.api.server.ApiServer` — nothing wires it into the daemon yet. `EventBroker` and the events
   subscription-command parsing (`parse_subscription_command`) were generalized out of their
   Tornado-specific bits so both bridges share the same code. The RPC executor here uses 4 workers
   instead of Tornado's 1, since `plugs.call()`'s own lock (see finding above) already provides the
   real serialization — more HTTP-layer workers just avoid queuing unrelated requests (e.g. `/health`)
   behind a slow plugin call. Tests: `test/api/test_fastapi_server.py`.
3. **Port the library endpoints** (upload, folders, entries, refresh — the streaming/multipart-heavy
   ones) to FastAPI.
4. **Port the WebSocket event broker** to FastAPI's WebSocket support; decide fate of the ZMQ pub/sub hop
   underneath (keep it, or replace with in-process asyncio queues now that everything's one process).
5. **Reassess the ZMQ REP/REQ layer** once FastAPI fully replaces Tornado — does it still earn its keep,
   or can CLI and webapp both call the same in-process FastAPI app / plugin dispatch directly and drop a
   hop?
6. **Remove the Tornado dependency**, and check what else assumed it: webapp nginx config
   (`resources/default-settings/nginx.default`), `installation/routines/setup_jukebox_webapp.sh`, ports
   referenced in config defaults.
7. **Measure before/after.** "High performance" needs a number, not a vibe — concurrent library scans,
   cover-art fetches, and RPC calls during active playback are the realistic stress cases.

## Relationship to the other fork tracks

- **Plugin system**: deliberately *not* pulling in upstream's `future3/draft-entrypoint-plugins` draft
  (two-tier core/user-plugin loading, config-toggled entry points). The goal here is more powerful
  plugins than that model supports — how deep a plugin can reach into playback, library, and the API
  layer is a question to design once this core architecture work has settled, not before. Revisit step 5
  above (plugin dispatch call sites) with that redesign in mind rather than migrating the old model.
- **Packaging/installer**: mostly orthogonal, but step 6 above (nginx/service file changes) overlaps with
  the "ship resources as package data" work already scoped in
  `documentation/developers/roadmap-plugins-and-packaging.md` (Track B) — sequence so the same install
  routine isn't edited twice for unrelated reasons.
- **Naming**: deferred, no dependency.

## Open decisions

- Does ZMQ pub/sub for events survive, or get replaced by in-process asyncio primitives once nothing
  needs the `ZMQStream` bridge? (`FastApiServer` still uses ZMQ SUB via `zmq.asyncio`, unchanged for now.)
- Does the CLI keep speaking ZMQ REP, or move to the FastAPI HTTP API / plugin dispatch directly?
- Concurrency model for `plugs.call()`: replace the single global `_lock_module` with per-component
  locking (or async-aware dispatch) so unrelated plugin calls (e.g. library scan vs. playback control)
  don't serialize against each other. This is the actual "high performance" work — the FastAPI swap
  alone doesn't achieve it.
- Does `/api/v1` get replaced in place, or versioned to `/api/v2` during the transition? (Currently:
  reused as-is by both bridges, since only one runs against real traffic at a time.)
