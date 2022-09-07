from typing import Dict, Optional

import wemulate.utils.tcconfig as tcutils
import wemulate.core.database.utils as dbutils
import wemulate.ext.utils.common as common
from wemulate.core.database.models import ConnectionModel


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


def delete_parameter(
    connection_name: str, parameters: Dict[str, int], direction: Optional[str]
) -> None:
    """
    Delete specific parameters on the given connection.
    If a direction is provided, the parameter will be removed only on the given direction.
    If not, the parameter will be removed in both directions (bidirectional, in-/outgoing).

    Args:
        connection_name: Name of the connection on which the parameters should be deleted.
        parameters: Parameters which should be deleted.
        direction: The direction on which the parameter should be removed (bidirectional if None)

    Returns:
        None
    """
    connection, current_parameters = common.get_current_applied_parameters(
        connection_name
    )
    physical_interface_name = dbutils.get_physical_interface_by_logical_interface_id(
        connection.first_logical_interface_id
    ).physical_name
    tcutils.remove_parameters(connection_name, physical_interface_name)
    common.set_parameters_with_tc(
        connection,
        common.delete_parameters_in_db(
            parameters, current_parameters, connection, direction
        ),
        direction,
    )
