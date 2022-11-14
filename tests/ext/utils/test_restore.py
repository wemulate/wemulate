from unittest.mock import MagicMock
from tests.helpers.database import (
    db_test_setup,
    create_one_connection,
    create_two_connections,
)
from wemulate.ext import utils as extutils
from wemulate.utils import tcconfig


def test_restore_device(db_test_setup):
    tcconfig.add_connection = MagicMock(return_value=True)
    tcconfig.set_parameters = MagicMock(return_value=True)
    create_two_connections()
    assert extutils.restore_device() is None


def test_restore_connection(db_test_setup):
    tcconfig.add_connection = MagicMock(return_value=True)
    tcconfig.set_parameters = MagicMock(return_value=True)
    create_one_connection()
    assert extutils.reset_connection("test") is None
