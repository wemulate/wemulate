import wemulate.core.database.utils as dbutils
import wemulate.ext.utils.common as common
from wemulate.core.database.models import ConnectionModel
from typing import Dict


def set_parameter(connection_name: str, parameters: Dict[str, int]) -> None:
    """
    Set parameters on the given connection. Replaces all parameters which are configured.

    Args:
        connection_name: Name of the connection on which the parameters should be configured.
        parameters: Parameters which should be configured.

    Returns:
        None
    """
    connection: ConnectionModel = dbutils.get_connection_by_name(connection_name)
    dbutils.delete_all_parameter_on_connection(connection.connection_id)
    common.set_parameters_with_tc(
        connection, common.create_or_update_parameters_in_db(connection, parameters)
    )
