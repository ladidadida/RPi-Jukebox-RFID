# migrate_to_cli

Everything here is slated to become functionality of the `jukebox` CLI (`packages/cli`) and is
not yet rewritten — see `documentation/developers/roadmap-core-architecture.md`,
"Packaging/install overhaul". It lives in its own top-level folder so it's obviously provisional
rather than mixed in with permanent code under `packages/`. Nothing left here has been rewritten;
it runs exactly as it did in its previous location.

- `installation/` — bash install routines run on a real Raspberry Pi
  (`install-jukebox.sh` + `routines/`). Eventual target: `jukebox setup ...`
  subcommands.
- `scripts/` — RFID registration and audio config setup tools. Both currently broken (they
  `import jukebox.hostif`, deleted along with the old plugin system) and blocked on a `hostif`
  redesign, so they're not ported to the CLI yet. Eventual target: `jukebox setup ...`
  subcommands.

`run_jukebox.py` and `run_publicity_sniffer.py` (and the `tools/` wrapper around the latter) have
already been ported and removed from here — see `jukebox run` / `jukebox debug sniff` in
`packages/cli`.

Do not add new permanent code here. If you're building new functionality, it belongs
in `packages/jukebox` or `packages/cli` instead.
