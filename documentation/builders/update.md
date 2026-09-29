# Update

- [Updating your Jukebox](#updating-your-jukebox)
- [Coming from an installation with the old installer](#coming-from-an-installation-with-the-old-installer)
- [Migration Path from Version 2](#migration-path-from-version-2)

## Updating your Jukebox

```bash
jukebox update --check     # is there a newer version?
jukebox update             # install it, re-apply the setup, restart the jukebox
```

- **Package installation** (the default of `install.sh`): installs the latest release from
  GitHub (`--version vX.Y.Z` for a specific one) into the jukebox's environment. Plugins you
  installed yourself stay, extra dependencies of enabled plugins are kept.
- **Source installation** (`install.sh --source`): `git pull` of the current branch, then
  `uv sync`; the web app is rebuilt if it changed and `npm` is installed.

Afterwards `jukebox setup --yes` re-applies the setup with your earlier answers (e.g. an updated
service definition) and a running jukebox service is restarted.

Your data -- music, settings, cards -- lives in the jukebox home (`jukebox home` shows it) and is
not touched by an update. Cards in the old format are converted when the jukebox starts (with a
backup of the card database).

## Coming from an installation with the old installer

Installations made with the old `install-jukebox.sh` keep their data in `~/RPi-Jukebox-RFID/shared`.
Either keep using that checkout as a source installation:

```bash
cd ~/RPi-Jukebox-RFID && git pull
curl -fsSL https://raw.githubusercontent.com/ladidadida/RPi-Jukebox-RFID/main/install.sh | bash -s -- --source ~/RPi-Jukebox-RFID
```

or install the package and point it at the old data:

```bash
curl -fsSL https://raw.githubusercontent.com/ladidadida/RPi-Jukebox-RFID/main/install.sh | bash -s -- --home ~/RPi-Jukebox-RFID/shared
```

Paths written by the old installer (`../../shared/...`) are understood. The old system service
(`/usr/lib/systemd/user/jukebox-daemon.service`) is overridden by the one `jukebox setup` writes to
`~/.config/systemd/user/`.

## Migration path from Version 2

There is no update path coming from Version 2.x of the Jukebox.
You need to do a fresh install of Version 3 on a fresh Raspberry Pi OS image.
See [Installing Phoniebox future3](./installation.md).

> [!IMPORTANT]
> Do start with a fresh SD card image!

Do not just pull the future3 branch into you existing Version 2.x directory.
Do not run the installer on an system that had Version 2.x running before on it.
Stuff has changed too much to make this feasible.
