from typing import Dict, List
from wemulate.core.exc import WEmulateConfigNotFoundError

import netifaces, yaml


def get_config_path() -> str:
    return "/etc/wemulate/wemulate.yml"


def _get_config() -> Dict:
    try:
        with open(get_config_path()) as file:
            return yaml.full_load(file)
    except FileNotFoundError:
        raise WEmulateConfigNotFoundError


def get_mgmt_interfaces() -> List[str]:
    return _get_config()["wemulate"]["management_interfaces"]


def get_interfaces() -> List[str]:
    return [
        name
        for name in netifaces.interfaces()
        if name.startswith(("eth", "en"))
        and name not in _get_config()["wemulate"]["management_interfaces"]
    ]


def get_db_location() -> str:
    return _get_config()["wemulate"]["db_location"]
