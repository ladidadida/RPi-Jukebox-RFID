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
│   │   ├── jukebox/        Framework: Component-Registry, FastAPI-API-Bridge (HTTP + WebSocket +
│   │   │                   Webapp-Static-Files + /logs, ersetzt RPC-Server und nginx), In-Process-
│   │   │                   Pub/Sub-Bus, Config-Handling. Kein ZeroMQ mehr im ganzen Projekt.
│   │   ├── components/     Explizit von jukebox.daemon verdrahtet (kein Plugin-System mehr):
│   │   │                   player, rfid, publishing, misc. Andere frühere Komponenten (gpio,
│   │   │                   mqtt, volume, timers, battery_monitor, controls, jingle, hostif,
│   │   │                   synchronisation) wurden entfernt, kommen später neu gestaltet zurück.
│   │   ├── misc/           Utility-Code
│   │   └── run_*.py        Einstiegspunkte (Core, RFID-Registrierung, Audio-Config, Publicity-Sniffer)
│   └── webapp/              React-Frontend (Touch-/Web-UI), kommuniziert per HTTP/WebSocket
│       │                    mit der FastAPI-Bridge (`/api/v1/*`)
│       ├── src/             Components, Contexts, Sockets, Commands
│       └── public/          Statische Assets, i18n-Übersetzungen (de/en)
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
├── tools/                        Dev-/Debug-CLI-Tools (Publicity-Sniffer)
├── ci/                           CI-Hilfsskripte (u. a. Installationstests)
├── AGENTS.md / CLAUDE.md          Anleitung für KI-Coding-Agenten
├── CONTRIBUTING.md                Contributor-Richtlinien (Namenskonventionen, PR-Prozess)
├── pyproject.toml / bam.yaml      Python-Tooling (uv, ruff, pyright, pytest) + Task-Runner
└── uv.lock                        Gepinnte Dependency-Versionen (uv)
```

## Architektur in Kürze

Siehe `documentation/developers/roadmap-core-architecture.md` für den aktuellen Stand und offene
Punkte. Kurzfassung:

1. **Component-Registry** (`jukebox.registry`) — ersetzt das alte, config-getriebene
   Plugin-System. `jukebox.daemon.run()` verdrahtet jede Komponente explizit
   (`register()`/`start()`), nichts wird mehr dynamisch aus der Config geladen.
2. **FastAPI als Browser-Bridge** — HTTP (`/api/v1/rpc`, Library-Endpoints), WebSocket
   (`/api/v1/events`), und seit Kurzem auch das Webapp-Static-Build + `/logs` direkt (kein nginx
   mehr davor). RFID-Kartenaktionen laufen direkt in-process über die Registry. ZeroMQ ist komplett
   raus: sowohl das Python-RPC-CLI (`run_rpc_tool.py`) als auch der C-Client
   (`src/cli_client/pbc.c`) und der ZMQ-REP-Server wurden entfernt. Aktuell gibt es kein
   CLI-Tool mehr; ein Ersatz auf Basis des FastAPI-Endpoints ist geplant, aber noch nicht entworfen.
3. **In-Process Pub/Sub-Bus** (`jukebox.publishing`, `EventBus`) — Status/Events, thread-sicher,
   kein ZeroMQ mehr. Die Webapp und `run_publicity_sniffer.py` abonnieren über die
   FastAPI-WebSocket-Bridge.

Die Musikwiedergabe läuft über **MPD (Music Player Daemon)**, angesteuert per `python-mpd2`.

## Eingesetzte Tools und Libraries

### Python-Kern (`packages/jukebox`)

| Zweck | Library |
|---|---|
| RFID/USB/Bluetooth-Eingabe | `evdev` |
| Audio-Tags lesen | `mutagen` |
| PulseAudio-Steuerung | `pulsectl` |
| MPD-Client | `python-mpd2` |
| Konfigurationsdateien (YAML) | `ruamel.yaml` |
| HTTP-Requests (Playlist-Generator) | `requests` |
| HTTP/WebSocket-API | `fastapi`, `uvicorn` |
| Publicity-Sniffer (WebSocket-Client) | `websockets` |
| GPIO (Raspberry Pi) | `rpi-lgpio` (lgpio-Shim für Bookworm-Kompatibilität), `gpiozero` |
| Code-Qualität | `ruff`, `pyright`, `pytest`, `pytest-cov`, `mock` |
| API-Doku-Generierung | `pydoc-markdown` |

Kein ZeroMQ mehr (siehe `documentation/developers/roadmap-core-architecture.md`). Minimale
Python-Version: **3.11**.

### Web-App (`packages/webapp`, React/JavaScript)

| Zweck | Library |
|---|---|
| Framework/Build | React 17, Create React App (`react-scripts`) |
| UI-Komponenten | MUI v5 (`@mui/material`, `@mui/icons-material`), Emotion |
| Routing | `react-router-dom` |
| Internationalisierung | `i18next`, `react-i18next`, `i18next-browser-languagedetector`, `i18next-http-backend` |
| RPC/Events im Browser | native `fetch`/`WebSocket` gegen die FastAPI-Bridge (`/api/v1/*`), kein ZeroMQ mehr |
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
uv run python packages/jukebox/scripts/run_jukebox.py
```

Die Webapp wird separat mit npm gebaut/gestartet (`cd packages/webapp && npm start`).

## Nützliche Kommandos (aus dem Repo-Root)

Paketmanager ist **uv**, der Dev-/CI-Workflow läuft über **bam** (`bam.yaml`, content-addressed
Task-Runner mit Caching). Die alten `run_*.sh`-Wrapper-Skripte gibt es nicht mehr.

```bash
uv sync --group dev              # .venv anlegen/aktualisieren (Runtime + Dev-Dependencies)
uv run python packages/jukebox/scripts/run_jukebox.py   # Jukebox Core starten
bam lint                         # ruff check (gecached)
bam format                       # ruff format (Auto-Fix)
bam test                         # pytest, schreibt .reports/junit.xml
bam typecheck                    # pyright (aktuell nur informativ, siehe Roadmap)
bam docs                         # API-Doku neu generieren (pydoc-markdown)
bam markdownlint                 # Markdown-Doku linten
bam ci-checks                    # alles, was auch CI prüft, in einem Kommando
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
