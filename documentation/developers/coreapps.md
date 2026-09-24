# Jukebox Apps

The Jukebox core and its developer tools are exposed through the `jukebox` CLI (`packages/cli`).
To learn more about each command and its parameters, run:

``` bash
$ uv run jukebox <command> --help
```

RFID/audio setup tools are not part of the CLI yet -- see "Configuration Tools" below.

## Jukebox Core

**Command:** `jukebox run` (run via `uv run jukebox run`)

This is the main app. It starts the Jukebox Core.

This runs as a service, which starts automatically after boot-up. At times, it may be necessary to restart the service, for example, after a configuration change. Not all configuration changes can be applied on-the-fly. See [Jukebox Configuration](../builders/configuration.md#jukebox-configuration).

For debugging, it's best to run Jukebox directly from the console rather than as a service, as this provides direct logging information in the console and allows for changing command line parameters. See [Troubleshooting](../builders/troubleshooting.md).

The player backend is selected via `player.backend` in the Jukebox configuration (default:
`local_audio`, no extra install needed). Non-default backends (`mpd`) and GPIO-attached RFID
readers need their dependencies installed first: `uv sync --extra mpd`, `uv sync --extra
rpi-gpio`, or the extra matching a specific bundled reader module (see AGENTS.md).

## Configuration Tools

Before running the configuration tools, stop the Jukebox Core service.
See [Best practice procedure](../builders/configuration.md#best-practice-procedure).

### Audio

**Scriptname:** [setup_configure_audio.sh](../../migrate_to_cli/installation/components/setup_configure_audio.sh)

A setup tool to select the primary and secondary audio sinks used by the Jukebox.

Run this once after installation. It can be re-run at any time to change the
selected outputs. For more information see
[Audio Configuration](../builders/audio.md).

### RFID Reader

**Scriptname:** [setup_rfid_reader.sh](../../migrate_to_cli/installation/components/setup_rfid_reader.sh)

Setup tool to configure the RFID Readers.

Run this once to register and configure the RFID readers with Jukebox. It can be re-run at any time to change the settings. For more information see [RFID Readers](./rfid/README.md).

> [!NOTE]
> This tool will always create a new configuration file, thereby overwriting the old one (after confirming with the user). Any manual modifications to the settings will need to be reapplied.

## Developer Tools

### RPC

There is no dedicated RPC CLI tool right now. Both previous ones were removed -- the interactive
Python tool (`run_rpc_tool.py` / `tools/run_rpc_tool.sh`) and the C client
(`src/cli_client/pbc.c`), along with the ZeroMQ REP server they talked to
(`jukebox.rpc.server.RpcServer`). A replacement, built against the FastAPI `/api/v1/rpc` HTTP
endpoint, is planned but not designed yet -- see
`documentation/developers/roadmap-core-architecture.md`. In the meantime, `curl` or any HTTP
client can call `POST /api/v1/rpc` directly with a `{"package": ..., "plugin": ..., "method": ...}`
JSON body.

### Publicity Sniffer

**Command:** `jukebox debug sniff` (run via `uv run jukebox debug sniff`)

This command-line tool monitors all messages sent from Jukebox through the publishing interface, printing received messages in the console. It is primarily used for debugging.
