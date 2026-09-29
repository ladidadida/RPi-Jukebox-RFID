from dotenv import load_dotenv

# Must run before app() is invoked below: JUKEBOX_CONF/JUKEBOX_LOGGER_CONF (typer.Option
# `envvar`s in jukebox_cli.run) are only read from os.environ when the command actually runs,
# not at import time -- but populating them any later than this would be too late. Searches for
# a `.env` file starting from the current directory and walking up, same convention this
# project already uses everywhere else (repo root as working directory).
load_dotenv()

from pathlib import Path  # noqa: E402
from typing import Optional  # noqa: E402

import typer  # noqa: E402

import jukebox.paths  # noqa: E402
from jukebox_cli import debug  # noqa: E402
from jukebox_cli.run import run  # noqa: E402

app = typer.Typer(name="jukebox", help="Jukebox CLI.")


@app.callback()
def main(home: Optional[Path] = typer.Option(
        None, "--home", envvar=jukebox.paths.HOME_ENV,
        help="Directory with all jukebox data (settings, music, logs). "
             "Default: $XDG_DATA_HOME/jukebox (~/.local/share/jukebox).")) -> None:
    jukebox.paths.set_home(home)


@app.command(name="home")
def show_home() -> None:
    """Print the jukebox home and the configuration file in use."""
    typer.echo(f"home:   {jukebox.paths.home()}")
    typer.echo(f"config: {jukebox.paths.settings_dir() / 'jukebox.yaml'}")


app.command(name="run")(run)
app.add_typer(debug.app, name="debug")
