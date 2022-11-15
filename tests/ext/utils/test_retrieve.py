from typing import List
from tests.helpers.database import (
    db_test_setup,
    create_one_connection,
    create_two_connections,
)
from wemulate.ext import utils as extutils
from wemulate.core.database.models import ConnectionModel


def test_get_physical_interface_names(db_test_setup):
    assert extutils.get_physical_interface_names("LAN-A", "LAN-B") == ("ens4", "ens5")


def test_get_logical_interface_by_name(db_test_setup):
    assert extutils.get_logical_interface_by_name("LAN-A").logical_name == "LAN-A"


def test_connection_exists_in_db(db_test_setup):
    create_one_connection()
    assert extutils.connection_exists_in_db("test")


def test_get_connection_by_name(db_test_setup):
    create_one_connection()
    assert extutils.get_connection_by_name("test").connection_name == "test"


def test_get_connection_by_id(db_test_setup):
    create_one_connection()
    assert extutils.get_connection_by_id(1).connection_name == "test"


def test_get_logical_interface_by_id(db_test_setup):
    assert extutils.get_logical_interface_by_id(1).logical_name == "LAN-A"


def test_get_logical_interface_by_physical_name(db_test_setup):
    assert (
        extutils.get_logical_interface_by_physical_name("ens4").logical_name == "LAN-A"
    )


def test_get_connection_list(db_test_setup):
    create_two_connections()
    connection_list: List[ConnectionModel] = extutils.get_connection_list()
    assert len(connection_list) == 2
    for conn in connection_list:
        if conn.connection_name == "test1":
            assert True
        if conn.connection_name == "test2":
            assert True
