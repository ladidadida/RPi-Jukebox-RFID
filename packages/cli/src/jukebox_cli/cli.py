import typer

from jukebox_cli import debug
from jukebox_cli.run import run

app = typer.Typer(name="jukebox", help="Jukebox CLI.")
app.command(name="run")(run)
app.add_typer(debug.app, name="debug")
