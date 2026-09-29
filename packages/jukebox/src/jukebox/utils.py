"""
Common utility functions
"""
import logging
import subprocess


log = logging.getLogger('jb.utils')


def get_config_action(cfg, section, option, default, valid_actions_dict, logger):
    """
    Looks up the given {section}.{option} config option and returns
    the associated entry from valid_actions_dict, if valid. Falls back to the given
    default otherwise.
    """
    action = cfg.setndefault(section, option, value='').lower()
    if action not in valid_actions_dict:
        logger.error(f"Config {section}.{option} must be one of {valid_actions_dict.keys()}. Using default '{default}'")
        action = default
    return valid_actions_dict[action]


def get_git_state():
    """Return git state information for the current branch"""

    gitlog = "No git log info"
    try:
        sub = subprocess.run("git log --pretty='%h [%cs] %s %d' -n 1 --no-color",
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             check=True)
        gitlog = sub.stdout.decode('utf-8').strip()
    except Exception as e:
        log.error(f"{e.__class__.__name__}: {e}")

    describe = "No git describe info"
    try:
        sub = subprocess.run("git describe --always --dirty",
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             check=True)
        if sub.returncode == 0:
            describe = sub.stdout.decode('utf-8').strip()
    except Exception as e:
        log.error(f"{e.__class__.__name__}: {e}")

    return f"{gitlog} [{describe}]"
