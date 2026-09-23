# migrate_to_cli

Everything here is slated to become functionality of a future `jukebox` CLI
(`packages/cli`) and is not yet rewritten — see
`documentation/developers/roadmap-core-architecture.md`, "Packaging/install overhaul".
It lives in its own top-level folder so it's obviously provisional rather than mixed in
with permanent code under `packages/`. Nothing in here has been rewritten; it runs
exactly as it did in its previous location.

- `installation/` — bash install routines run on a real Raspberry Pi
  (`install-jukebox.sh` + `routines/`). Eventual target: `jukebox setup ...`
  subcommands.
- `scripts/` — launcher scripts (jukebox core, RFID registration, audio config,
  publicity sniffer). Eventual target: `jukebox run` / `jukebox setup ...` /
  `jukebox debug ...` subcommands.
- `tools/` — dev wrapper for the publicity sniffer.

Do not add new permanent code here. If you're building new functionality, it belongs
in `packages/jukebox` or `packages/cli` instead.
