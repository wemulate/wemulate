from typing import Dict, Optional

import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils
import wemulate.ext.utils.common as common
from wemulate.ext.utils import retrieve


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
    dbutils.create_connection(
        connection_name,
        dbutils.get_logical_interface_by_name(first_logical_interface),
        dbutils.get_logical_interface_by_name(second_logical_interface),
        dbutils.get_active_profile(dbutils.get_device()),
    )
    tcutils.add_connection(
        connection_name,
        physical_interface1_name,
        physical_interface2_name,
    )


def add_parameter(
    connection_name: str, parameters: Dict[str, int], direction: Optional[str]
) -> None:
    """
    Add parameters to the already configured parameters on the given connection.
    If a direction is provided, the parameter will be applied only on the given direction.
    If not, the parameter will be applied in both directions (bidirectional, in-/outgoing).

    Args:
        connection_name: Name of the connection on which the parameters should be configured.
        parameters: Parameters which should be configured.
        direction: Direction on which the parameter should be applied (bidirectional if None)

    Returns:
        None
    """
    connection, current_parameters = common.get_current_applied_parameters(
        connection_name
    )
    common.set_parameters_with_tc(
        connection,
        common.create_or_update_parameters_in_db(
            connection, parameters, direction, current_parameters
        ),
        direction,
    )
