from unittest.mock import MagicMock
from typing import List
from tests.helpers.database import (
    db_test_setup,
    create_one_connection,
    create_two_connections,
)
from wemulate.ext import utils as extutils
from wemulate.core.database import utils as dbutils
from wemulate.core.database.models import ConnectionModel
from wemulate.utils import tcconfig


def test_reset_device(db_test_setup):
    tcconfig.remove_parameters = MagicMock(return_value=True)
    tcconfig.remove_connection = MagicMock(return_value=True)
    create_two_connections()
    extutils.reset_device()
    connection_list: List[ConnectionModel] = dbutils.get_connection_list()
    assert connection_list == []


def test_reset_connection(db_test_setup):
    tcconfig.remove_parameters = MagicMock(return_value=True)
    create_one_connection()
    extutils.reset_connection("test")
    connection: ConnectionModel = dbutils.get_connection_by_name("test")
    assert connection.parameters == []
