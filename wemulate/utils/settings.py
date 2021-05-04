from wemulate.core.exc import WEmulateConfigNotFound, WEmulateError
import netifaces, yaml


def get_config_path():
    return "/etc/wemulate/wemulate.yml"


def _get_config():
    try:
        with open("/etc/wemulate/wemulate.yml") as file:
            config = yaml.full_load(file)
        return config
    except FileNotFoundError:
        raise WEmulateConfigNotFound 


def get_mgmt_interfaces():
    return _get_config()["wemulate"]["management_interfaces"]


def get_interfaces():
    return [
        name
        for name in netifaces.interfaces()
        if name.startswith(("eth", "en"))
        and name not in _get_config()["wemulate"]["management_interfaces"]
    ]


def get_db_location():
    return _get_config()["wemulate"]["db_location"]