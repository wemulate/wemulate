import netifaces, yaml

def _get_config():
    with open('/etc/wemulate/wemulate.yml') as file:
        config = yaml.full_load(file)
    return config

def get_mgmt_interfaces():
    return _get_config()['wemulate']['management_interfaces']

def get_interfaces():
    return [name for name in netifaces.interfaces() if name.startswith(("eth", "en")) and name not in _get_config()['wemulate']['management_interfaces'] ]