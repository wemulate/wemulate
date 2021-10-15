import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils
import wemulate.ext.utils.common as common
from wemulate.ext.utils import retrieve
from typing import Dict
from wemulate.core.database.models import ConnectionModel


def add_connection(
    connection_name: str, first_logical_interface: str, second_logical_interface: str
) -> None:
    """
    Creates a new connection in the database and adds a linux bridge on the host system.

    Args:
        connection_name: Name of the connection which should be created.
        first_logical_interface: Name of the first logical interface.
        second_logical_interface: Name of the second logical interface.

    Returns:
        None
    """
    (
        physical_interface1_name,
        physical_interface2_name,
    ) = retrieve.get_physical_interface_names(
        first_logical_interface, second_logical_interface
    )
    tcutils.add_connection(
        connection_name,
        physical_interface1_name,
        physical_interface2_name,
    )
    dbutils.create_connection(
        connection_name,
        dbutils.get_logical_interface_by_name(first_logical_interface),
        dbutils.get_logical_interface_by_name(second_logical_interface),
        dbutils.get_active_profile(dbutils.get_device(1)),
    )


def add_parameter(connection_name: str, parameters: Dict[str, int]) -> None:
    """
    Add parameters to the already configured parameters on the given connection.

    Args:
        connection_name: Name of the connection on which the parameters should be configured.
        parameters: Parameters which should be configured.

    Returns:
        None
    """
    connection: ConnectionModel = dbutils.get_connection_by_name(connection_name)
    current_parameters: Dict[str, int] = {
        parameter.parameter_name: parameter.value for parameter in connection.parameters
    }
    common.set_parameters_with_tc(
        connection,
        common.create_or_update_parameters_in_db(
            connection, parameters, current_parameters
        ),
    )
