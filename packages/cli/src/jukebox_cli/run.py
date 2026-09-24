import logging
import os
from pathlib import Path

import typer

import jukebox.cfghandler
import jukebox.daemon
from jukebox.misc import loggingext

#: Template a missing --logger file is created from on first run (see run(), below).
DEFAULT_LOGGER_CONFIG_TEMPLATE = 'resources/default-settings/logger.default.yaml'


def _default_config_dir() -> Path:
    """XDG-style per-user config directory: $XDG_CONFIG_HOME/jukebox, or ~/.config/jukebox."""
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
    base = Path(xdg_config_home) if xdg_config_home else Path.home() / '.config'
    return base / 'jukebox'


def run(
    conf: Path = typer.Option(
        _default_config_dir() / 'jukebox.yaml', "-c", "--conf",
        envvar="JUKEBOX_CONF",
        file_okay=True, dir_okay=False,
        help="Jukebox configuration file. Created from the default template on first run if it "
             "doesn't exist yet. Default is $XDG_CONFIG_HOME/jukebox/jukebox.yaml (or "
             "~/.config/jukebox/jukebox.yaml) -- this repo's own .env overrides that to "
             "shared/settings/jukebox.yaml for development.",
    ),
    logger_conf: Path = typer.Option(
        _default_config_dir() / 'logger.yaml', "-l", "--logger",
        envvar="JUKEBOX_LOGGER_CONF",
        file_okay=True, dir_okay=False,
        help="Logger configuration file. Created from the default template on first run if it "
             "doesn't exist yet. Same default location as --conf.",
    ),
    verbose: int = typer.Option(
        0, "-v", "--verbose", count=True,
        help="Increase logger verbosity from warning to info (-v) to debug (-vv) to see all "
             "plugin calls and not only errors (-vvv)",
    ),
    quiet: int = typer.Option(
        0, "-q", "--quiet", count=True,
        help="Decrease logger verbosity from warning to error (-q) to critical (-qq)",
    ),
    artifacts: bool = typer.Option(
        False, "-a", "--artifacts",
        help="Write out all artifacts and auto-generated help files",
    ),
) -> None:
    """Start the Jukebox Daemon."""
    if verbose and quiet:
        raise typer.BadParameter("--verbose and --quiet are mutually exclusive")

    if verbose:
        logger = loggingext.configure_default({1: logging.INFO, 2: logging.DEBUG}[min(verbose, 2)],
                                               with_publisher=True)
        if verbose < 3:
            loggingext.configure_default(logging.ERROR, name='jb.plugin.call', with_publisher=True)
    elif quiet:
        logger = loggingext.configure_default({1: logging.ERROR, 2: logging.CRITICAL}[min(quiet, 2)],
                                               with_publisher=True)
    else:
        jukebox.cfghandler.ensure_default_config(str(logger_conf), DEFAULT_LOGGER_CONFIG_TEMPLATE)
        logger = loggingext.configure_from_file(str(logger_conf))

    logger.info(f"Using jukebox configuration file '{conf}'")
    myjukebox = jukebox.daemon.get_jukebox_daemon(str(conf), artifacts)
    myjukebox.run()
