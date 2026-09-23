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
                   player (MPD), rfid, publishing, system (formerly "misc" RPC calls), misc
                   (shared utility code). Other former components (gpio, mqtt, volume, timers,
                   battery_monitor, controls, jingle, hostif, synchronisation) were removed and
                   will come back as new, not-yet-designed components.
  cli/             Scaffold for a future CLI (jukebox-cli) — empty stub, not implemented yet
  webapp/          React front-end (the touch/web UI), talks to the core via HTTP/WebSocket
                   (FastAPI, `/api/v1/*`). Not a uv workspace member (npm/Vite project), but lives
                   alongside the Python packages structurally.
migrate_to_cli/    Working area for everything slated to become CLI functionality and not yet
                   rewritten (see documentation/developers/roadmap-core-architecture.md,
                   "Packaging/install overhaul") — moved here so it's obviously provisional rather
                   than mixed in with permanent code. Runs exactly as before, just relocated:
  installation/    Bash install routines run on a real Raspberry Pi (install-jukebox.sh +
                   routines/) — the eventual target is `jukebox setup ...` CLI subcommands
  scripts/         Launcher scripts (jukebox core, RFID registration, audio config, publicity
                   sniffer) — the eventual target is `jukebox run` / `jukebox setup ...` /
                   `jukebox debug ...` CLI subcommands
  tools/           Dev wrapper for the publicity sniffer
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
  (`run_rpc_tool.py`), and the C CLI client (`src/cli_client/pbc.c`) were all removed. No CLI tool
  currently exists; a replacement built on the FastAPI endpoint is planned but not designed yet
  (see roadmap).
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
uv run python migrate_to_cli/scripts/run_jukebox.py   # start the Jukebox core
bam lint                        # ruff check (cached)
bam format                      # ruff format (auto-fix)
bam format-check                # ruff format --check (informational only for now, see roadmap)
bam typecheck                   # pyright (informational only for now, see roadmap)
bam test                        # pytest, writes .reports/junit.xml
bam docs                        # regenerate API docs (pydoc-markdown)
bam markdownlint                # lint markdown docs (needs packages/webapp/node_modules)
bam ci-checks                   # everything CI runs, in one command
migrate_to_cli/tools/run_publicity_sniffer.sh   # print all messages on the publishing queue
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
