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
pyproject.toml     uv workspace root (virtual: no [project] table); shared dev-tool config
                   (ruff/pyright/pytest/coverage/pydoc-markdown) lives here
packages/          uv workspace members
  jukebox/         Python core application ("Jukebox Core") — the daemon that runs on the Pi
    pyproject.toml Real [project] table (package=true), runtime dependencies, hatchling backend
    src/jukebox/   The installable package: explicit component registry, FastAPI API bridge
                   (api/), in-process pub/sub event bus (publishing/), config handling, and the
                   components explicitly wired by jukebox.daemon at start-up (no plugin/
                   config-driven loading — see documentation/developers/roadmap-core-architecture.md):
                   player, rfid, publishing, system (formerly "misc" RPC calls), misc (shared
                   utility code). Other former components (gpio, mqtt, volume, timers,
                   battery_monitor, controls, jingle, hostif, synchronisation) were removed and
                   will come back as new, not-yet-designed components.
  cli/             Jukebox CLI (jukebox-cli). Implemented so far: `jukebox run` (start the daemon),
                   `jukebox debug sniff` (publishing-bus WebSocket sniffer). `jukebox setup ...`
                   (install routines) is not implemented yet — still in migrate_to_cli/.
  webapp/          React front-end (the touch/web UI), talks to the core via HTTP/WebSocket
                   (FastAPI, `/api/v1/*`). Not a uv workspace member (npm/Vite project), but lives
                   alongside the Python packages structurally.
migrate_to_cli/    Working area for everything slated to become CLI functionality and not yet
                   rewritten (see documentation/developers/roadmap-core-architecture.md,
                   "Packaging/install overhaul") — moved here so it's obviously provisional rather
                   than mixed in with permanent code. Runs exactly as before, just relocated:
  installation/    Bash install routines run on a real Raspberry Pi (install-jukebox.sh +
                   routines/) — the eventual target is `jukebox setup ...` CLI subcommands
  scripts/         RFID registration and audio config setup tools -- both currently broken (import
                   jukebox.hostif, removed along with the old plugin system) and blocked on a
                   hostif redesign; not yet ported to the CLI. run_jukebox.py/run_publicity_sniffer.py
                   were replaced by `jukebox run`/`jukebox debug sniff` and removed from here.
docker/            Dockerfiles + compose files for a non-Pi development environment
resources/         Default settings, systemd services, sample audio, autohotspot configs
shared/            Runtime data: audiofolders, playlists, settings, logs (mounted/shared at runtime)
documentation/     Project docs: builders/ (end users/installers) and developers/ (contributors)
test/              Python unit tests (pytest)
ci/                CI helper scripts (e.g. installation testing)
```

## Architecture essentials

- **Component registry**: `jukebox.registry` (replacing the old `jukebox.plugs` dynamic plugin
  system) is a minimal explicit call registry. `jukebox.daemon.run()` wires up each component
  (currently: publishing, system, player, rfid) directly by calling its `register()`/`start()`
  functions — nothing is loaded from config anymore. Call addressing (`package`, `plugin`,
  `method`) is unchanged, so the webapp's RPC call shape didn't need to change.
- **RPC**: the Web App (via `POST /api/v1/rpc`) and RFID card swipes (direct in-process calls)
  both dispatch through the *same* `(package, plugin, method)` call shape — read
  `documentation/builders/rpc-commands.md` before adding a new user-triggerable action. ZeroMQ is
  gone entirely now: the old ZMQ REP server (`jukebox.rpc.server`), the Python RPC CLI
  (`run_rpc_tool.py`), and the C CLI client (`src/cli_client/pbc.c`) were all removed. A first CLI
  slice now exists (`packages/cli`, `jukebox run`/`jukebox debug sniff`), but a dedicated RPC tool
  built on the FastAPI `/api/v1/rpc` endpoint is still not designed (see roadmap).
- **Publishing event bus** (`jukebox.publishing`, backed by `jukebox.publishing.bus.EventBus`):
  the status/event channel components publish to (`publishing.get_publisher().send(topic,
  payload)`) — thread-safe, in-process, no ZMQ involved anymore (see
  documentation/developers/roadmap-core-architecture.md, "Simplify away ZMQ and nginx"). The
  webapp subscribes via the FastAPI WebSocket bridge (`/api/v1/events`); `jukebox debug sniff`
  connects there too as a plain WebSocket client.
- **Player backend**: pluggable, selected via `player.backend` config -- see "Player/RFID backends
  are pluggable" below. Default is `local_audio` (decodes via PyAV, outputs via sounddevice/
  PortAudio, no external process); `mpd` (an external mpd server, via `python-mpd2`) is an opt-in
  alternative. Both implement the same duck-typed surface `player.coordinator.PlayerCoordinator`
  calls on the active backend.
- Playback/config data lives under `shared/` (audiofolders, playlists, settings, logs) — this is
  what gets mounted into Docker containers and is where user-editable YAML config sits.
- **Player/RFID backends are pluggable** (first slice of the "Advanced plugin system" track, see
  `documentation/developers/roadmap-core-architecture.md`): `player.backend` config picks the
  player backend (`jukebox.player.plugin` dispatches to it by `importlib.import_module`, mirroring
  how `jukebox.rfid.reader` already loads a hardware reader module by name); non-default backends'
  dependencies are `pyproject.toml` extras (`mpd`, `rpi-gpio`, and one per bundled RFID reader
  module), not installed by default -- run `uv sync --extra <name>` to add one. This is what makes
  the Pi/mpd/GPIO-specific pieces optional rather than a hard dependency of the core app.

## Languages, tools, conventions

- **Python** (core, min version 3.11): PEP 8 style, enforced by **ruff** (`[tool.ruff]` in
  `pyproject.toml`, max line 127, max-complexity 12 — mirrors the old flake8 config, not yet
  running ruff's isort/pyupgrade rules or `ruff format` on the existing tree, see
  `documentation/developers/roadmap-core-architecture.md`). All Python plugin/config folder & file
  names are `snake_case`, descriptive, general→specific (see `CONTRIBUTING.md` "Naming
  conventions" section) — this is a deliberate v2→v3 break, follow it strictly.
- **JavaScript/React** (`packages/webapp`): Create React App (`react-scripts`), MUI v5, i18next for
  translations (`de`/`en` under `packages/webapp/public/locales`), Ramda, react-router-dom.
- **Config format**: YAML (`ruamel.yaml`), defaults in `resources/default-settings/`.
- Everything under any `scratch*`-named folder is git- and ruff-ignored — safe scratch space,
  never a place for real code.

## Common commands (run from repo root)

Package manager is **uv**; the dev/CI workflow is driven by **[bam](https://gitlab.com/cascascade/bam)**
(`bam.yaml`), a content-addressed task runner — cached, so re-running an unchanged task is instant.
The old `run_*.sh` wrapper scripts are gone.

```bash
uv sync --group dev             # install/update the .venv (runtime + dev dependencies)
                                 # add --extra mpd / --extra rpi-gpio / --extra <reader-name> for
                                 # non-default player/RFID backends (see "Player/RFID backends
                                 # are pluggable" above) -- not needed for the default local_audio
                                 # backend or the generic_usb/fake_reader_gui readers
uv run jukebox run              # start the Jukebox core -- creates shared/settings/jukebox.yaml
                                 # and logger.yaml from the default templates on first run if
                                 # missing. Override the paths with -c/-l or $JUKEBOX_CONF/
                                 # $JUKEBOX_LOGGER_CONF.
bam lint                        # ruff check (cached)
bam format                      # ruff format (auto-fix)
bam format-check                # ruff format --check (informational only for now, see roadmap)
bam typecheck                   # pyright (informational only for now, see roadmap)
bam test                        # pytest, writes .reports/junit.xml
bam docs                        # regenerate API docs (pydoc-markdown)
bam markdownlint                # lint markdown docs (needs packages/webapp/node_modules)
bam ci-checks                   # everything CI runs, in one command
bam build                       # build the webapp into packages/webapp/build/, so `jukebox run`
                                 # alone serves both the API and the UI on :5556 -- no npm start
                                 # needed just to use the app (no hot-reload though; for active
                                 # frontend dev use `cd packages/webapp && npm run dev` instead)
bam docker-dev                  # local mpd+jukebox+webapp stack without PulseAudio/hardware
uv run jukebox debug sniff      # print all messages on the publishing queue
```

Webapp (`cd packages/webapp`): standard CRA scripts — `npm start`, `npm run build`, `npm test`.

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

The default `player.backend: local_audio` + `generic_usb`/`fake_reader_gui` RFID readers need no
Pi-specific hardware or extra system packages at all -- `uv run jukebox run` plays through this
machine's normal audio output directly. The Docker dev environment
(`documentation/developers/docker.md`) is still useful for testing the full stack (core + webapp
+ nginx-free FastAPI static serving) in isolation, but is no longer required just to avoid GPIO/
mpd/RFID hardware.

## Key docs to read before larger changes

- `documentation/builders/concepts.md` — plugin interface / RPC / pub-sub in one page
- `documentation/builders/rpc-commands.md` — RPC command reference
- `documentation/developers/coreapps.md` — what each core entry-point script does
- `documentation/developers/python.md` — Python dev environment notes
- `documentation/developers/webapp.md` — webapp dev notes
- `documentation/developers/docker.md` — Docker-based dev environment
- `documentation/developers/status.md` — feature parity status vs. v2
