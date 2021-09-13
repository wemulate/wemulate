import yaml
from typing import Dict
from wemulate.core.exc import WEmulateConfigNotFoundError


def get_config_path() -> str:
    """
    Returns the current path of the config.

    Returns:
        Returns the path as string.
    """
    return "/etc/wemulate/wemulate.yml"


def get_config() -> Dict:
    """
    Returns the current configuration as dict.

    Returns:
        Returns the whole configuration as dict.
    """
    try:
        with open(get_config_path()) as file:
            return yaml.full_load(file)
    except FileNotFoundError:
        raise WEmulateConfigNotFoundError


def get_db_location() -> str:
    """
    Returns the current database path from the configuration file.

    Returns:
        Returns the path to the database as string.
    """
    return get_config()["wemulate"]["db_location"]
