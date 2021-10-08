import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils
from wemulate.core.database.models import ConnectionModel


def reset_device() -> None:
    """
    Deletes all parameters and connection in the database and on the host system.

    Returns:
        None
    """
    for connection in dbutils.get_connection_list():
        physical_interface_name = (
            dbutils.get_physical_interface_by_logical_interface_id(
                connection.first_logical_interface_id
            ).physical_name
        )
        tcutils.remove_parameters(connection.connection_name, physical_interface_name)
        tcutils.remove_connection(connection.connection_name)
    dbutils.reset_all_connections()


def reset_connection(connection_name: str) -> None:
    """
    Creates a new connection in the database and adds a linux bridge on the host system.

    Args:
        connection_name: Name of the connection which should be reset

    Returns:
        None
    """
    connection: ConnectionModel = dbutils.get_connection_by_name(connection_name)
    dbutils.delete_all_parameter_on_connection(connection.connection_id)
    physical_interface_name = dbutils.get_physical_interface_by_logical_interface_id(
        connection.first_logical_interface_id
    ).physical_name
    tcutils.remove_parameters(connection.connection_name, physical_interface_name)
