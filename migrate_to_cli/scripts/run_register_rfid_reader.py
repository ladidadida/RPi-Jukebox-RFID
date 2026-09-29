#!/usr/bin/env python
"""
Setup tool to configure the RFID Readers.

Run this once to register and configure the RFID readers with the Jukebox. Can be re-run at any time to change
the settings. For more information see [RFID Readers](../rfid/README.md).

> [!NOTE]
> This tool will always write a new configurations file. Thus, overwrite the old one (after checking with the user).
> Any manual modifications to the settings will have to be re-applied

"""
import os
import logging
import argparse
import subprocess

import jukebox.cfghandler
import jukebox.misc.inputminus as pyil
import jukebox_rfid_readers.configure as rfid_configure

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Create console handler and set default level
logconsole = logging.StreamHandler()
logconsole.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s: %(message)s',
                                          datefmt='%d.%m.%Y %H:%M:%S'))
logconsole.setLevel(logging.INFO)
logger.addHandler(logconsole)


def jukebox_service_active() -> bool:
    result = subprocess.run(['systemctl', '--user', 'is-active', '--quiet', 'jukebox-daemon'], check=False)
    return result.returncode == 0


def enable_driver_plugins(jukebox_config: str, config_dict: dict) -> None:
    """List the driver plugin of every configured reader under 'plugins:' in the jukebox config."""
    drivers = {reader['module'] for reader in config_dict['rfid']['readers'].values()}
    if not drivers or not os.path.exists(jukebox_config):
        return
    cfg = jukebox.cfghandler.get_handler('jukebox')
    jukebox.cfghandler.load_yaml(cfg, jukebox_config)
    for driver in sorted(drivers):
        cfg.setndefault('plugins', f'rfid_{driver}', value={})
    cfg.save(only_if_changed=True)
    print(f"Enabled reader driver plugins in '{jukebox_config}': {', '.join(f'rfid_{d}' for d in sorted(drivers))}")


def main():
    # The default config file relative to this files location and independent of working directory
    script_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    cfg_file_default = os.path.abspath(os.path.join(script_path, '../../shared/settings/rfid.yaml'))
    jukebox_cfg_default = os.path.abspath(os.path.join(script_path, '../../shared/settings/jukebox.yaml'))

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force",
                        help="Force overwriting of existing configuration",
                        action="store_true", default=False)
    parser.add_argument("-d", "--deps",
                        help="Install dependencies: (a)uto, (n)o, (q)uery [default]",
                        metavar="CHAR", choices=['a', 'q', 'n', 'auto', 'query', 'no'], default='q')
    parser.add_argument("-c", "--conffile",
                        help=f"Output configuration file [default: '{cfg_file_default}']",
                        metavar="FILE", default=cfg_file_default)
    parser.add_argument("-j", "--jukebox-conffile",
                        help=f"Jukebox configuration to enable the driver plugins in [default: '{jukebox_cfg_default}']",
                        metavar="FILE", default=jukebox_cfg_default)
    parser.add_argument("-v", "--verbosity",
                        help="Increase verbosity to 'DEBUG'",
                        action="store_true", default=False)
    args = parser.parse_args()

    if args.verbosity is True:
        print("Setting logging level to DEBUG.")
        logconsole.setLevel(logging.DEBUG)

    if jukebox_service_active():
        pyil.msg_highlight('Jukebox service is running!')
        print("\nPlease stop jukebox-daemon service and restart tool")
        print("$ systemctl --user stop jukebox-daemon\n\n")
        print("Don't forget to start the service again :-)")
        return

    dinstall_lookup = {'a': 'auto', 'q': 'query', 'n': 'no', 'auto': 'auto', 'query': 'query', 'no': 'no'}
    config_dict = rfid_configure.query_user_for_reader(dependency_install=dinstall_lookup[args.deps])
    rfid_configure.write_config(args.conffile, config_dict, force_overwrite=args.force)
    enable_driver_plugins(args.jukebox_conffile, config_dict)


if __name__ == '__main__':
    main()
