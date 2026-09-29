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
    src/jukebox/   The installable package: the core/plugin contract (contract/), the core
                   modules (core_modules.py: system, player, cards, rfid), FastAPI API bridge
                   (api/), in-process event bus (publishing/), config handling. Removed former
                   components come back as core modules (volume, timers, jingle, system info,
                   input devices) or plugins (raspberry-pi, mqtt, card sync) -- see
                   documentation/developers/core-and-plugins.md.
    interfaces/    Interface snapshots of the framework contract and every core module, checked
                   by test/contract/test_snapshots.py (see "Core and plugins" below)
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

- **Core and plugins** (`jukebox.contract`, design in `documentation/developers/core-and-plugins.md`):
  every piece of functionality is a *module*: a `CoreModule` (always shipped, always running,
  listed in `jukebox/core_modules.py`) or a `Plugin` (separate package, found via the
  `jukebox.plugins` entry-point group, loaded only when listed under `plugins:` in jukebox.yaml).
  Start order comes from `requires`. Modules declare operations with `@action` (state-changing:
  REST route + card action `<module>.<action>` + in-process call) and `@query` (read-only GET),
  typed events with `event(name, Model)` (topic `<module>.<name>`), and extension points
  (`player.backends`, `rfid.readers`). Everything must be type-annotated; argument models are
  built from the signature. Don't hand-write REST routes or card aliases for new functionality --
  declare them on a module. Per-module lock by default (`concurrency = 'threadsafe'` opts out).
- **Interface versioning**: each module has an `interface_version`, the framework a
  `CONTRACT_VERSION`. Snapshots in `packages/jukebox/interfaces/` (and `interface.json` in bundled
  plugin packages) are compared in CI: a breaking change (removed/renamed operation or field,
  type change, protocol change) needs a major bump, an addition a minor bump. After bumping, run
  `uv run python -m jukebox.contract.snapshots --update` and commit the snapshot.
- **API**: the webapp talks to routes generated from the modules' operations (`/api/v1/player/*`,
  `/api/v1/settings`, `/api/v1/cards`, ... -- see `/docs` on the running daemon), plus
  `GET /api/v1/modules` (active modules, their operations/events, skipped plugins) and
  `GET /api/v1/actions` (card actions with argument schemas). Card entries, card removal actions
  and the second-swipe action are stored as `action: <module>.<action>` plus named `args`
  (`documentation/builders/actions.md`); the old alias/package-plugin-method format is converted
  by `jukebox.legacy_actions` (cards.yaml is migrated on start-up with a backup). ZeroMQ, the
  generic HTTP RPC endpoint and the old call registry are gone. A first CLI slice exists
  (`packages/cli`, `jukebox run`/`jukebox debug sniff`), but a dedicated CLI for the API is not
  designed yet.
- **Event bus** (`jukebox.publishing.get_bus()`, a `jukebox.publishing.bus.EventBus`): thread-safe,
  in-process, last-value cached. Modules publish typed events through `ctx.publish(event,
  payload)` (validated against the event's model; raises with `JUKEBOX_STRICT=1`, logs and drops
  otherwise), never untyped dicts. The
  webapp subscribes via the FastAPI WebSocket bridge (`/api/v1/events`); `jukebox debug sniff`
  connects there too as a plain WebSocket client.
- **Player backend**: registered at the `player.backends` extension point, selected via
  `player.backend` config. Default is `local_audio` (decodes via PyAV, outputs via sounddevice/
  PortAudio, no external process); `mpd` (an external mpd server, via `python-mpd2`) is an opt-in
  alternative. Backends implement `jukebox.player.backend.PlayerBackend`; the player module turns
  their raw status into the typed `player.status` event (`jukebox.player.status.PlayerStatus`).
- Playback/config data lives under `shared/` (audiofolders, playlists, settings, logs) — this is
  what gets mounted into Docker containers and is where user-editable YAML config sits.
- **Optional dependencies**: non-default player backends and RFID reader drivers still come
  from `pyproject.toml` extras (`mpd`, `rpi-gpio`, one per bundled reader driver) until they move
  into plugin packages -- run `uv sync --extra <name>` to add one.

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

- `documentation/developers/core-and-plugins.md` — core/plugin contract design
- `documentation/builders/concepts.md` — core, plugins, actions, events in one page
- `documentation/builders/actions.md` — action format for cards and config
- `documentation/developers/coreapps.md` — what each core entry-point script does
- `documentation/developers/python.md` — Python dev environment notes
- `documentation/developers/webapp.md` — webapp dev notes
- `documentation/developers/docker.md` — Docker-based dev environment
- `documentation/developers/status.md` — feature parity status vs. v2
