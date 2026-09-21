# Projektübersicht: RPi-Jukebox-RFID (future3)

Stand: 2026-07-18, Branch `future3/develop`

## Was ist das Projekt?

Phoniebox / RPi-Jukebox-RFID ist eine RFID-gesteuerte Musikbox für den Raspberry Pi: Man hält
eine RFID-Karte an ein Lesegerät, die Box spielt eine dazu hinterlegte Playlist/ein Album ab —
ganz ohne Bildschirm oder App-Zwang (die Zielgruppe sind oft Kinder). `future3` ist ein
kompletter Neuentwurf ("re-write") der älteren Version 2, mit neuen Namenskonventionen und
Architektur. Es existiert parallel weiter die stabile Version 2 im `main`-Zweig des Original-Repos.

## Ordnerstruktur

```
.
├── src/
│   ├── jukebox/            Python-Kernanwendung ("Jukebox Core"), läuft als Daemon auf dem Pi
│   │   ├── jukebox/        Framework: Plugin-Loader, RPC-Server, Publish/Subscribe, Config-Handling
│   │   ├── components/     Plugins (dynamisch geladen): player, playermpd, rfid, gpio, mqtt,
│   │   │                   volume, timers, battery_monitor, controls, jingle, hostif,
│   │   │                   synchronisation, publishing
│   │   ├── misc/           Utility-Code
│   │   └── run_*.py        Einstiegspunkte (Core, RPC-Tool, RFID-Registrierung, Audio-Config, Sniffer)
│   ├── webapp/              React-Frontend (Touch-/Web-UI), kommuniziert per RPC/ZeroMQ (WebSocket)
│   │   ├── src/             Components, Contexts, Sockets, Commands
│   │   └── public/          Statische Assets, i18n-Übersetzungen (de/en)
│   └── cli_client/           Kommandozeilen-Client
├── installation/             Bash-Installationsroutinen für den echten Raspberry Pi
│   ├── install-jukebox.sh    Haupt-Installer
│   ├── routines/             Einzelne Installationsschritte (MPD, RFID, Autohotspot, Samba, …)
│   ├── components/           Wiederverwendbare Setup-Skripte (Audio, RFID, HiFiBerry)
│   └── options/               Optionale Zusatzfeatures
├── docker/                    Dockerfiles + docker-compose für eine Nicht-Pi-Entwicklungsumgebung
├── resources/                  Default-Settings, systemd-Services, Beispiel-Audio, Autohotspot-Configs
├── shared/                     Laufzeitdaten: audiofolders, playlists, settings, logs
│                                (wird in Docker gemountet, enthält die vom Nutzer editierbare
│                                 jukebox.yaml)
├── documentation/               Projektdokumentation
│   ├── builders/                 Für Endanwender/Installateure (Installation, Konfiguration, GPIO, RFID, …)
│   └── developers/                Für Mitwirkende (Python, Webapp, Docker, RPC, Architekturkonzepte)
├── test/                         Python-Unittests (pytest)
├── tools/                        Dev-/Debug-CLI-Tools (RPC-Tool, Publicity-Sniffer)
├── ci/                           CI-Hilfsskripte (u. a. Installationstests)
├── AGENTS.md / CLAUDE.md          Anleitung für KI-Coding-Agenten
├── CONTRIBUTING.md                Contributor-Richtlinien (Namenskonventionen, PR-Prozess)
└── run_*.sh                       Wrapper-Skripte (Jukebox starten, Tests, Linting, Doku-Generierung)
```

## Architektur in Kürze

Die Core-App basiert auf drei Konzepten (siehe `documentation/builders/concepts.md`):

1. **Plugin-Interface** — Pakete unter `src/jukebox/components` werden zur Laufzeit anhand der
   Konfiguration geladen, initialisiert und beendet. Fehlschlagende Plugins werden übersprungen,
   nicht fatal (Logs prüfen!).
2. **RPC-Server (Remote Procedure Call)** — Web-App, RFID-Kartenerkennung, GPIO-Tasten und das
   CLI-Tool `run_rpc_tool.py` lösen Aktionen alle über denselben RPC-Mechanismus aus. Transport
   erfolgt über **ZeroMQ** (`pyzmq` im Core, `jszmq` im Webapp).
3. **Publishing Message Queue** — Gegenstück zum RPC: Der Core publiziert Status/Events, die
   Webapp und der `run_publicity_sniffer.py` abonnieren diese.

Die Musikwiedergabe läuft über **MPD (Music Player Daemon)**, angesteuert per `python-mpd2`.

## Eingesetzte Tools und Libraries

### Python-Kern (`src/jukebox`)

| Zweck | Library |
|---|---|
| RFID/USB/Bluetooth-Eingabe | `evdev` |
| Audio-Tags lesen | `mutagen` |
| ALSA-Audio | `pyalsaaudio` |
| PulseAudio-Steuerung | `pulsectl` |
| MPD-Client | `python-mpd2` |
| Konfigurationsdateien (YAML) | `ruamel.yaml` |
| HTTP-Requests (Playlist-Generator) | `requests` |
| Event-Loop / Publisher | `tornado` |
| GPIO (Raspberry Pi) | `rpi-lgpio` (lgpio-Shim für Bookworm-Kompatibilität), `gpiozero` |
| RPC-Transport | `pyzmq` (ZeroMQ) |
| MQTT-Integration | `paho-mqtt` |
| Code-Qualität | `flake8`, `pytest`, `pytest-cov`, `mock` |
| API-Doku-Generierung | `pydoc-markdown` |

Minimale Python-Version: **3.9**.

### Web-App (`src/webapp`, React/JavaScript)

| Zweck | Library |
|---|---|
| Framework/Build | React 17, Create React App (`react-scripts`) |
| UI-Komponenten | MUI v5 (`@mui/material`, `@mui/icons-material`), Emotion |
| Routing | `react-router-dom` |
| Internationalisierung | `i18next`, `react-i18next`, `i18next-browser-languagedetector`, `i18next-http-backend` |
| RPC/ZeroMQ im Browser | `jszmq` |
| Funktionale Utilities | `ramda` |
| Tests | `@testing-library/react`, `@testing-library/jest-dom` |
| Markdown-Linting | `markdownlint-cli2` |

### Infrastruktur / Sonstiges

- **MPD** als Wiedergabe-Backend, **PulseAudio/ALSA** für Audio-Routing.
- **Docker & Docker Compose** für eine Pi-unabhängige Entwicklungsumgebung (separate Container für
  Core, MPD, Webapp).
- **systemd** für die Diensteinrichtung auf dem Pi (`resources/default-services`).
- **MQTT** (paho-mqtt) für optionale Smart-Home-/Automatisierungs-Integration.
- **GitHub Actions** für CI (Python-Tests, Doku-Checks, Installationstests unter Debian/Docker).
- **Coveralls** für Testabdeckung.

## Installation

Es gibt zwei grundsätzliche Wege:

### 1. Auf einem echten Raspberry Pi (Produktivbetrieb)

1. Raspberry Pi OS Lite (Legacy, 32-bit) mit dem Raspberry Pi Imager aufspielen (SSH + WLAN direkt
   beim Flashen konfigurieren).
2. Auf dem Pi einloggen und den Installer ausführen — Details in
   `documentation/builders/installation.md`. Kernstück ist `installation/install-jukebox.sh`,
   das über `installation/routines/*.sh` u. a. folgende Schritte orchestriert:
   - System-Pakete installieren (`packages-core.txt`, per `apt-get`)
   - Python-`.venv` anlegen und Dependencies aus `pyproject.toml` per `uv sync` installieren
   - MPD, Audio (PulseAudio/ALSA), RFID-Reader, Autohotspot/WLAN, Samba, Kiosk-Modus (Webapp im
     Vollbild) einrichten
   - systemd-Services registrieren
3. Konfiguration erfolgt über YAML-Dateien in `shared/settings` (Vorlage:
   `resources/default-settings/jukebox.default.yaml`).

### 2. Lokale Entwicklungsumgebung (Docker, ohne Pi-Hardware)

Für Beiträge, die keine GPIO-/RFID-Hardware benötigen — siehe `documentation/developers/docker.md`:

```bash
git clone https://github.com/MiczFlor/RPi-Jukebox-RFID.git
cp ./resources/default-settings/jukebox.default.yaml ./shared/settings/jukebox.yaml
# jukebox.yaml mit docker/config/jukebox.overrides.yaml zusammenführen
# MP3-Testdateien nach ./shared/audiofolders kopieren
docker-compose -f docker/docker-compose.yml up   # ggf. plattformspezifische Compose-Datei (mac/linux)
```

Docker, Compose und (host-seitig) PulseAudio müssen vorher installiert sein; je nach Host
(Mac/Linux/Windows) sind zusätzliche Audio-Konfigurationsschritte nötig (siehe Doku).

### 3. Manuelles Python-Setup (nur Core, ohne Installer)

```bash
uv sync --group dev
# ggf. vorher: sudo apt install libasound2-dev
uv run python src/jukebox/run_jukebox.py
```

Die Webapp wird separat mit npm gebaut/gestartet (`cd src/webapp && npm start`).

## Nützliche Kommandos (aus dem Repo-Root)

Paketmanager ist **uv**, der Dev-/CI-Workflow läuft über **bam** (`bam.yaml`, content-addressed
Task-Runner mit Caching). Die alten `run_*.sh`-Wrapper-Skripte gibt es nicht mehr.

```bash
uv sync --group dev              # .venv anlegen/aktualisieren (Runtime + Dev-Dependencies)
uv run python src/jukebox/run_jukebox.py   # Jukebox Core starten
bam lint                         # ruff check (gecached)
bam format                       # ruff format (Auto-Fix)
bam test                         # pytest, schreibt .reports/junit.xml
bam typecheck                    # pyright (aktuell nur informativ, siehe Roadmap)
bam docs                         # API-Doku neu generieren (pydoc-markdown)
bam markdownlint                 # Markdown-Doku linten
bam ci-checks                    # alles, was auch CI prüft, in einem Kommando
tools/run_rpc_tool.sh            # interaktives RPC-CLI gegen laufenden Core
tools/run_publicity_sniffer.sh   # alle Publish-Nachrichten mitlesen
```

## Sonstiges Erwähnenswertes

- **Strenge Namenskonvention** (siehe `CONTRIBUTING.md`): alle Datei-/Ordnernamen klein geschrieben,
  Wörter mit Unterstrich getrennt (keine Bindestriche — Konflikt mit Python-Modulnamen!), vom
  Allgemeinen zum Speziellen benannt. Dies ist ein bewusster Bruch mit den Namenskonventionen von
  Version 2.
- **`scratch*`-Ordner** sind auf allen Ebenen von Git und flake8 ausgeschlossen — gedacht als lokaler
  Experimentierbereich.
- **Git-Hooks** werden mitgeliefert, aber nicht automatisch aktiviert:
  `cp .githooks/pre-commit .git/hooks/.` (Checks vor Commit) und
  `cp .githooks/post-merge .git/hooks/.` (Hinweis auf nötige Dependency-Updates nach Pull).
- **PR-Konventionen**: Trivialänderungen dürfen die Commit-/PR-Präfixe `(docs)`, `(maint)` oder
  `(packaging)` statt einer Ticketnummer verwenden. Ziel-Branch für PRs ist standardmäßig
  `future3/develop`, nicht `future3/main`.
- **Testabdeckung ist aktuell gering** — laut `CONTRIBUTING.md` ausdrücklich ein bekannter
  Schwachpunkt; neue Module sollten nach Möglichkeit Tests mitbringen.
- **Feature-Parität zu Version 2** ist noch nicht vollständig — Fortschritt wird in
  `documentation/developers/status.md` getrackt; das Projekt befindet sich damit noch in einer
  Übergangsphase zwischen v2 (produktiv, stabil) und future3 (in aktiver Entwicklung).
- **Community/Kommunikation** läuft über Matrix-Chat (`#phoniebox_community:gitter.im`) und
  GitHub Issues/PRs; es gibt einen jährlichen Community-Kalender (`documentation/calendars/`).
- **Lizenz**: siehe `LICENSE` im Root.
