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
  jukebox/         Core framework: plugin loader, RPC server, publishing/pubsub, config handling
  components/      Plugins loaded dynamically: player (MPD), rfid, gpio, mqtt, volume, timers,
                   battery_monitor, controls, jingle, hostif, synchronisation, publishing
  misc/            Shared utility code
  run_*.py         Entry points (jukebox core, RPC tool, RFID registration, audio config, sniffer)
src/webapp/        React front-end (the touch/web UI), talks to the core via RPC/ZeroMQ over WebSocket
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

- **Plugin interface**: the core app dynamically loads packages from `src/jukebox/components`
  based on config. Each plugin registers functions callable via RPC. A failing plugin is skipped
  at startup (check logs), not fatal.
- **RPC server**: the Web App, RFID card swipes, GPIO button presses, and the `run_rpc_tool.py`
  CLI all trigger core functionality through the *same* RPC protocol — read
  `documentation/builders/rpc-commands.md` before adding a new user-triggerable action.
  Transport is ZeroMQ (`pyzmq` / `jszmq` on the webapp side).
- **Publishing message queue**: the complementary status/event channel the core publishes to;
  the webapp and `run_publicity_sniffer.py` subscribe to it.
- **Player backend**: MPD (Music Player Daemon), driven via `python-mpd2`.
- Playback/config data lives under `shared/` (audiofolders, playlists, settings, logs) — this is
  what gets mounted into Docker containers and is where user-editable YAML config sits.

## Languages, tools, conventions

- **Python** (core, min version 3.9): PEP 8 style, enforced by **flake8** (`.flake8`, max line
  127, max-complexity 12). All Python plugin/config folder & file names are `snake_case`,
  descriptive, general→specific (see `CONTRIBUTING.md` "Naming conventions" section) — this is a
  deliberate v2→v3 break, follow it strictly.
- **JavaScript/React** (`src/webapp`): Create React App (`react-scripts`), MUI v5, i18next for
  translations (`de`/`en` under `src/webapp/public/locales`), Ramda, react-router-dom.
- **Config format**: YAML (`ruamel.yaml`), defaults in `resources/default-settings/`.
- Everything under any `scratch*`-named folder is git- and flake8-ignored — safe scratch space,
  never a place for real code.

## Common commands (run from repo root)

```bash
./run_jukebox.sh              # start the Jukebox core (activates .venv, runs src/jukebox/run_jukebox.py)
./run_pytest.sh                # run Python test suite (pytest -c pytest.ini), testpaths = test/
./run_flake8.sh                 # lint Python (flake8 --config .flake8)
./run_markdownlint.sh            # lint markdown docs (needs src/webapp/node_modules)
./run_docgeneration.sh           # regenerate API docs (pydoc-markdown)
tools/run_rpc_tool.sh            # interactive/one-shot RPC CLI against a running core
tools/run_publicity_sniffer.sh   # print all messages on the publishing queue
```

All Python runner scripts expect a `.venv` at the repo root
(`python -m pip install --no-cache-dir -r requirements.txt`); they `source .venv/bin/activate`
before running, and will fail loudly if it's missing.

Webapp (`cd src/webapp`): standard CRA scripts — `npm start`, `npm run build`, `npm test`.

## Before committing / opening a PR

- If you touched **any** `.py` file: run `./run_flake8.sh` and fix findings (or justify exceptions
  in the PR).
- Run `./run_pytest.sh` if you touched code with test coverage, and add tests for new modules
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
