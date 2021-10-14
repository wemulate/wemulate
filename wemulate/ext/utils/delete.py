import wemulate.utils.tcconfig as tcutils
import wemulate.core.database.utils as dbutils
import wemulate.ext.utils.common as common
from wemulate.core.database.models import ConnectionModel
from typing import Dict


def delete_connection(connection_name: str) -> None:
    """
    Delete connection with the given name.

    Args:
        connection_name: Name of the connection which should be deleted.

    Returns:
        None
    """
    connection: ConnectionModel = dbutils.get_connection_by_name(connection_name)
    physical_interface_name = dbutils.get_physical_interface_by_logical_interface_id(
        connection.first_logical_interface_id
    ).physical_name
    tcutils.remove_parameters(connection_name, physical_interface_name)
    tcutils.remove_connection(connection_name)
    dbutils.delete_connection_by_name(connection_name)


def delete_parameter(connection_name: str, parameters: Dict[str, int]) -> None:
    """
    Delete specific parameters on the given connection.

    Args:
        connection_name: Name of the connection on which the parameters should be deleted.
        parameters: Parameters which should be deleted.

    Returns:
        None
    """
    connection: ConnectionModel = dbutils.get_connection_by_name(connection_name)
    current_parameters: Dict[str, int] = {
        parameter.parameter_name: parameter.value for parameter in connection.parameters
    }

    physical_interface_name = dbutils.get_physical_interface_by_logical_interface_id(
        connection.first_logical_interface_id
    ).physical_name
    tcutils.remove_parameters(connection_name, physical_interface_name)
    common.set_parameters_with_tc(
        connection,
        common.delete_parameters_in_db(parameters, current_parameters, connection),
    )
