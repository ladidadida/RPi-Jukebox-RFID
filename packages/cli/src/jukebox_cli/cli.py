from dotenv import load_dotenv

# Must run before app() is invoked below: JUKEBOX_CONF/JUKEBOX_LOGGER_CONF (typer.Option
# `envvar`s in jukebox_cli.run) are only read from os.environ when the command actually runs,
# not at import time -- but populating them any later than this would be too late. Searches for
# a `.env` file starting from the current directory and walking up, same convention this
# project already uses everywhere else (repo root as working directory).
load_dotenv()

import typer  # noqa: E402

from jukebox_cli import debug  # noqa: E402
from jukebox_cli.run import run  # noqa: E402

app = typer.Typer(name="jukebox", help="Jukebox CLI.")
app.command(name="run")(run)
app.add_typer(debug.app, name="debug")
