from configparser import ConfigParser

import jukebox.paths


def test_pipewire_pulse_is_required_and_ordered():
    service_path = jukebox.paths.resource('default-services', 'jukebox-daemon.service')
    service = ConfigParser(interpolation=None)
    service.read(service_path)

    unit = service['Unit']
    assert 'pipewire-pulse.service' in unit['Requires'].split()
    assert 'pipewire-pulse.service' in unit['After'].split()
