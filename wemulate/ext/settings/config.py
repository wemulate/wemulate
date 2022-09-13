import yaml
from typing import Dict

from wemulate.core.exc import WEmulateConfigNotFoundError, WEmulateDatabaseError


WEMULATE_CONFIG_PATH = "/etc/wemulate/wemulate.yml"


def get_config_path() -> str:
    """
    Returns the current path of the config.

    Returns:
        Returns the path as string.
    """
    return WEMULATE_CONFIG_PATH


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
    try:
        return get_config().get("wemulate", {})["db_location"]
    except KeyError:
        raise WEmulateDatabaseError
