import wemulate.ext.utils.common as common
import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils

from wemulate.core.database.models import INCOMING, OUTGOING


def restore_device() -> None:
    """
    Restores all connections and tc parameters stored in the database.

    Returns:
        None
    """
    for connection in dbutils.get_connection_list():
        restore_connection(connection.connection_name)


def restore_connection(connection_name: str) -> None:
    """
    Restores a specific connection with its parameters stored in the database.

    Args:
        connection_name: Name of the connection which should be restored

    Returns:
        None
    """
    connection, current_parameter_in_db = common.get_current_applied_parameters(
        connection_name
    )

    physical_interface1_name = dbutils.get_physical_interface_by_logical_interface_id(
        connection.first_logical_interface_id
    ).physical_name
    physical_interface2_name = dbutils.get_physical_interface_by_logical_interface_id(
        connection.second_logical_interface_id
    ).physical_name
    tcutils.add_connection(
        connection_name, physical_interface1_name, physical_interface2_name
    )

    common.set_parameters_with_tc(
        connection, current_parameter_in_db, [INCOMING, OUTGOING]
    )
