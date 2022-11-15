from unittest.mock import MagicMock
from tests.helpers.database import db_test_setup, create_one_connection
from wemulate.ext import utils as extutils
from wemulate.core.database import utils as dbutils
from wemulate.core.database.models import (
    ConnectionModel,
    DELAY,
    INCOMING,
)
from wemulate.utils import tcconfig


def test_delete_connection(db_test_setup):
    create_one_connection()
    tcconfig.remove_parameters = MagicMock(return_value=True)
    tcconfig.remove_connection = MagicMock(return_value=True)
    extutils.delete_connection("test")
    connection: ConnectionModel = dbutils.get_connection_by_name("test")
    assert connection == None


def test_delete_parameter(db_test_setup):
    create_one_connection()
    tcconfig.remove_parameters = MagicMock(return_value=True)
    tcconfig.set_parameters = MagicMock(return_value=True)
    extutils.delete_parameter("test", {DELAY: 10}, INCOMING)
    connection: ConnectionModel = dbutils.get_connection_by_name("test")
    for param in connection.parameters:
        if param.parameter_name == DELAY and param.direction == INCOMING:
            assert False
