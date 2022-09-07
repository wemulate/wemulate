from typing import Dict, Optional

import wemulate.core.database.utils as dbutils
import wemulate.ext.utils.common as common
from wemulate.core.database.models import ConnectionModel


def set_parameter(
    connection_name: str, parameters: Dict[str, int], direction: Optional[str]
) -> None:
    """
    Set parameters on the given connection. Replaces all parameters which are configured.
    If a direction is provided, the parameter will be applied only on the given direction.
    If not, the parameter will be applied in both directions (bidirectional, in-/outgoing).

    Args:
        connection_name: Name of the connection on which the parameters should be configured.
        parameters: Parameters which should be configured.
        direction: Direction on which the parameter should be applied (bidirectional if None)

    Returns:
        None
    """
    connection: ConnectionModel = dbutils.get_connection_by_name(connection_name)
    dbutils.delete_all_parameter_on_connection(connection.connection_id, direction)
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
