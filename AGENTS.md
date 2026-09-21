# AGENTS.md

Guidance for AI coding agents (Claude, Codex, Copilot, etc.) working in this repository.

## What this project is

**Phoniebox / RPi-Jukebox-RFID — Version 3 ("future3")**: a complete rewrite of an RFID-controlled
audio jukebox for the Raspberry Pi. Kids (and others) tap an RFID card on a reader and the box
plays a specific playlist/album — no screen required. This branch (`future3/develop`) is a
from-scratch rewrite of the legacy (v2, shell-script based) project; do not assume v2 conventions
apply.

## Repository layout

```
src/jukebox/       Python core application ("Jukebox Core") — the daemon that runs on the Pi
  jukebox/         Core framework: explicit component registry, RPC server, FastAPI API bridge,
                   in-process pub/sub event bus, config handling
  components/      Explicitly wired by jukebox.daemon at start-up (no plugin/config-driven
                   loading — see documentation/developers/roadmap-core-architecture.md): player
                   (MPD), rfid, publishing, misc. Other former components (gpio, mqtt, volume,
                   timers, battery_monitor, controls, jingle, hostif, synchronisation) were
                   removed and will come back as new, not-yet-designed components.
  misc/            Shared utility code
  run_*.py         Entry points (jukebox core, RPC tool, RFID registration, audio config, sniffer)
src/webapp/        React front-end (the touch/web UI), talks to the core via HTTP/WebSocket
                   (FastAPI, `/api/v1/*`)
src/cli_client/    Command-line client
installation/      Bash install routines run on a real Raspberry Pi (install-jukebox.sh + routines/)
docker/            Dockerfiles + compose files for a non-Pi development environment
resources/         Default settings, systemd services, sample audio, autohotspot configs
shared/            Runtime data: audiofolders, playlists, settings, logs (mounted/shared at runtime)
documentation/     Project docs: builders/ (end users/installers) and developers/ (contributors)
test/              Python unit tests (pytest)
tools/             Dev/debug CLI tools (RPC tool, publicity sniffer)
ci/                CI helper scripts (e.g. installation testing)
```

## Architecture essentials

- **Component registry**: `jukebox.registry` (replacing the old `jukebox.plugs` dynamic plugin
  system) is a minimal explicit call registry. `jukebox.daemon.run()` wires up each component
  (currently: publishing, misc, player, rfid) directly by calling its `register()`/`start()`
  functions — nothing is loaded from config anymore. Call addressing (`package`, `plugin`,
  `method`) is unchanged, so the webapp's RPC call shape didn't need to change.
- **RPC server**: the Web App (via `POST /api/v1/rpc`), RFID card swipes (direct in-process calls),
  and the C CLI client (`src/cli_client/pbc.c`, still ZeroMQ REQ/REP against
  `jukebox.rpc.server.RpcServer`) all ultimately dispatch through the *same*
  `(package, plugin, method)` call shape — read `documentation/builders/rpc-commands.md` before
  adding a new user-triggerable action. The interactive Python RPC CLI (`run_rpc_tool.py`) was
  removed; a replacement isn't designed yet (see roadmap).
- **Publishing event bus** (`jukebox.publishing`, backed by `jukebox.publishing.bus.EventBus`):
  the status/event channel components publish to (`publishing.get_publisher().send(topic,
  payload)`) — thread-safe, in-process, no ZMQ involved anymore (see
  documentation/developers/roadmap-core-architecture.md, "Simplify away ZMQ and nginx"). The
  webapp subscribes via the FastAPI WebSocket bridge (`/api/v1/events`); `run_publicity_sniffer.py`
  connects there too as a plain WebSocket client.
- **Player backend**: MPD (Music Player Daemon), driven via `python-mpd2`.
- Playback/config data lives under `shared/` (audiofolders, playlists, settings, logs) — this is
  what gets mounted into Docker containers and is where user-editable YAML config sits.

## Languages, tools, conventions

- **Python** (core, min version 3.11): PEP 8 style, enforced by **ruff** (`[tool.ruff]` in
  `pyproject.toml`, max line 127, max-complexity 12 — mirrors the old flake8 config, not yet
  running ruff's isort/pyupgrade rules or `ruff format` on the existing tree, see
  `documentation/developers/roadmap-core-architecture.md`). All Python plugin/config folder & file
  names are `snake_case`, descriptive, general→specific (see `CONTRIBUTING.md` "Naming
  conventions" section) — this is a deliberate v2→v3 break, follow it strictly.
- **JavaScript/React** (`src/webapp`): Create React App (`react-scripts`), MUI v5, i18next for
  translations (`de`/`en` under `src/webapp/public/locales`), Ramda, react-router-dom.
- **Config format**: YAML (`ruamel.yaml`), defaults in `resources/default-settings/`.
- Everything under any `scratch*`-named folder is git- and ruff-ignored — safe scratch space,
  never a place for real code.

## Common commands (run from repo root)

Package manager is **uv**; the dev/CI workflow is driven by **[bam](https://gitlab.com/cascascade/bam)**
(`bam.yaml`), a content-addressed task runner — cached, so re-running an unchanged task is instant.
The old `run_*.sh` wrapper scripts are gone.

```bash
uv sync --group dev             # install/update the .venv (runtime + dev dependencies)
uv run python src/jukebox/run_jukebox.py   # start the Jukebox core
bam lint                        # ruff check (cached)
bam format                      # ruff format (auto-fix)
bam format-check                # ruff format --check (informational only for now, see roadmap)
bam typecheck                   # pyright (informational only for now, see roadmap)
bam test                        # pytest, writes .reports/junit.xml
bam docs                        # regenerate API docs (pydoc-markdown)
bam markdownlint                # lint markdown docs (needs src/webapp/node_modules)
bam ci-checks                   # everything CI runs, in one command
tools/run_publicity_sniffer.sh   # print all messages on the publishing queue
```

Webapp (`cd src/webapp`): standard CRA scripts — `npm start`, `npm run build`, `npm test`.

## Before committing / opening a PR

- If you touched **any** `.py` file: run `bam lint` and fix findings (or justify exceptions
  in the PR).
- Run `bam test` if you touched code with test coverage, and add tests for new modules
  under `test/`.
- Commit message prefixes `(docs)`, `(maint)`, `(packaging)` are used for trivial changes that
  don't need an issue number.
- Target branch is `future3/develop`, not `future3/main`, unless told otherwise.
- Full contributor guidelines: `CONTRIBUTING.md`.

## Testing without Raspberry Pi hardware

Prefer the Docker dev environment (`documentation/developers/docker.md`) over assuming real GPIO/
RFID hardware is present — it isolates MPD, the core, and the webapp into separate containers and
is the documented way to develop non-hardware-dependent parts of the app.

## Key docs to read before larger changes

- `documentation/builders/concepts.md` — plugin interface / RPC / pub-sub in one page
- `documentation/builders/rpc-commands.md` — RPC command reference
- `documentation/developers/coreapps.md` — what each core entry-point script does
- `documentation/developers/python.md` — Python dev environment notes
- `documentation/developers/webapp.md` — webapp dev notes
- `documentation/developers/docker.md` — Docker-based dev environment
- `documentation/developers/status.md` — feature parity status vs. v2
