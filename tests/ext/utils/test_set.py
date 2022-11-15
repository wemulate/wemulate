from unittest.mock import MagicMock
from typing import List
from tests.helpers.database import (
    db_test_setup,
    create_one_connection,
    create_two_connections,
)
from wemulate.ext import utils as extutils
from wemulate.core.database import utils as dbutils
from wemulate.core.database.models import ConnectionModel, BANDWIDTH, INCOMING
from wemulate.utils import tcconfig


def test_set_parameter(db_test_setup):
    tcconfig.set_parameters = MagicMock(return_value=True)
    create_one_connection()
    extutils.set_parameter("test", {BANDWIDTH: 100}, INCOMING)
    connection: ConnectionModel = dbutils.get_connection_by_id(1)
    count = 0
    for param in connection.parameters:
        if param.direction == INCOMING:
            count += 1
    assert count == 1
