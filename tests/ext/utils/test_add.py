from unittest.mock import MagicMock
from tests.helpers.database import db_test_setup
from wemulate.ext import utils as extutils
from wemulate.core.database import utils as dbutils
from wemulate.core.database.models import (
    ConnectionModel,
    LogicalInterfaceModel,
    DELAY,
    INCOMING,
    OUTGOING,
)
from wemulate.utils import tcconfig


def test_add_connection(db_test_setup):
    tcconfig.add_connection = MagicMock(return_value=True)
    extutils.add_connection("test", "LAN-A", "LAN-B")
    connection: ConnectionModel = dbutils.get_connection_by_name("test")
    first_logical_interface_id: LogicalInterfaceModel = (
        dbutils.get_logical_interface_by_name("LAN-A")
    )
    second_logical_interface_id: LogicalInterfaceModel = (
        dbutils.get_logical_interface_by_name("LAN-B")
    )
    assert connection.connection_name == "test"
    assert (
        connection.first_logical_interface_id
        == first_logical_interface_id.logical_interface_id
    )
    assert (
        connection.second_logical_interface_id
        == second_logical_interface_id.logical_interface_id
    )


def test_add_parameter(db_test_setup):
    tcconfig.set_parameters = MagicMock(return_value=True)
    extutils.add_connection("test", "LAN-A", "LAN-B")
    parameters = {DELAY: 10}
    extutils.add_parameter("test", parameters, INCOMING)

    connection: ConnectionModel = dbutils.get_connection_by_name("test")
    for param in connection.parameters:
        if param.parameter_name == DELAY:
            assert param.value == 10
            assert param.direction == INCOMING

    extutils.add_parameter("test", parameters, None)
    connection: ConnectionModel = dbutils.get_connection_by_name("test")
    count = 0
    for param in connection.parameters:
        if param.parameter_name == DELAY:
            assert param.value == 10
            if param.direction == INCOMING:
                count += 1
            if param.direction == OUTGOING:
                count += 1
    assert count == 2
