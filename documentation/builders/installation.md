# Installing Phoniebox future3

## Install Raspberry Pi OS Lite

> [!IMPORTANT]
> All Raspberry Pi models are supported. For sufficient performance, **we recommend Pi 2, 3 or Zero 2** (`ARMv7` models). Because Pi 1 or Zero 1 (`ARMv6` models) have limited resources, they are slower (during installation and start up procedure) and might require a bit more work! Pi 4 and 5 are an excess ;-)

Before you can install the Phoniebox software, you need to prepare your Raspberry Pi.

This instruction uses the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/). We recommend using the latest **Raspberry Pi OS Lite** image - Trixie.

### Raspberry Pi Imager

1. Connect a Micro SD card to your computer (preferable an SD card with high read throughput)
1. Start the Raspberry Pi Imager
1. Model: select "No filtering"
1. OS: select **Raspberry Pi OS (other)** and then **Raspberry Pi OS Lite** (64 bit, 32 bit should also work) - the version without Desktop environment
1. Storage: Select your Micro SD card (your card will be formatted)
1. Customize:
    * Hostname: choose hostname for the network (e.g. "phoniebox")
    * Localization: choose according to your location
    * User: choose a username and a password
    * Wifi: provide your wifi settings
    * Remote: enable SSH with "Use password authentication"
1. Click `Write`
1. Confirm the next warning about erasing the SD card with `Yes`
1. Wait for the imaging process to be finished (it'll take a few minutes)
1. Plug the SD into your Pi and optionally connect keyboard, monitor and mouse.

## Install Phoniebox software

Run the install script in your SSH terminal and follow the questions:

```bash
curl -fsSL https://raw.githubusercontent.com/ladidadida/RPi-Jukebox-RFID/main/install.sh | bash
```

It installs a few base packages and [uv](https://docs.astral.sh/uv/), then the jukebox from the
latest release, and finally runs `jukebox setup`, which asks what to set up on this machine
(Samba, WiFi hotspot, kiosk mode, RFID reader, boot optimisation, ...).

On a Raspberry Pi all jukebox data -- music, settings, logs -- lives in `~/jukebox`
(`JUKEBOX_HOME`); `jukebox home` shows where it is.

After a successful installation, [configure your Phoniebox](configuration.md).

> [!TIP]
> Depending on your hardware, this can take a while. Don't let your computer go to sleep, and
> consider running the installation in `screen` or `tmux`, so a dropped SSH connection doesn't
> interrupt it.

The Web App can upload files or complete folder trees, organize the audio library, and delete
files or folders, so Samba is off by default. Choose Samba when you also want direct network
access to the complete jukebox home, including configuration files. See [Samba](samba.md).

### Options

Pass options to the script with `bash -s --`, e.g.
`curl -fsSL .../install.sh | bash -s -- --source`:

| Option | Meaning |
| --- | --- |
| `--source [DIR]` | Install from a git checkout (default `~/RPi-Jukebox-RFID`) instead of the release packages |
| `--branch NAME` | Branch for `--source` (default `main`) |
| `--version TAG` | Install a specific release instead of the latest |
| `--repo OWNER/NAME` | Install from a fork |
| `--home DIR` | Where the jukebox keeps its data |
| `--yes` | Don't ask; use the defaults |
| `--no-setup` | Only install; run `jukebox setup` later |

### Changing the setup later

`jukebox setup` can be run again at any time; every step checks first and only changes what is
missing. Your earlier answers are remembered (`settings/setup.yaml` in the jukebox home).

```bash
jukebox setup --check      # what is set up, what is missing
jukebox setup samba        # run a single step (see: jukebox setup --list)
jukebox setup rfid         # configure an RFID reader
jukebox plugin list        # installed plugins; enable/disable them
```
