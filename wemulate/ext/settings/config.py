from typing import Dict
from pathlib import Path

WEMULATE_FOLDER_PATH = "/var/lib/wemulate"
WEMULATE_DATABASE_PATH = "/var/lib/wemulate/wemulate.db"


def get_db_location() -> str:
    """
    Returns the database path.

    Returns:
        Returns the path to the database as string.
    """
    return WEMULATE_DATABASE_PATH


def get_folder_location() -> str:
    """
    Returns the wemulate folder path.

    Returns:
        Returns the path to the wemulate folder as string.
    """
    return WEMULATE_FOLDER_PATH
