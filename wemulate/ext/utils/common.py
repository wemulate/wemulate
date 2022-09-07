from typing import Dict, Optional

import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils
from wemulate.core.database.models import (
    INCOMING,
    OUTGOING,
    PARAMETERS,
    ConnectionModel,
)


def _set_specific_parameter(
    connection: ConnectionModel,
    parameter_name: str,
    parameters: Dict[str, int],
    current_parameters: Dict[str, Dict[str, int]],
    direction: str,
) -> None:
    current_parameters[direction][parameter_name] = parameters[parameter_name]
    dbutils.create_or_update_parameter(
        connection.connection_id,
        parameter_name,
        parameters[parameter_name],
        direction,
    )


def get_current_applied_parameters(connection_name: str):
    """
    Retrieve the connection object and its current applied parameters.

    Args:
        connection_name: The name of the connection

    Returns:
        Returns the connection object (ConnectionModel) and the current_parameters which are currently set.
    """
    connection: ConnectionModel = dbutils.get_connection_by_name(connection_name)
    current_parameters: Dict[str, Dict[str, int]] = {OUTGOING: {}, INCOMING: {}}
    for parameter in connection.parameters:
        current_parameters[parameter.direction][
            parameter.parameter_name
        ] = parameter.value
    return connection, current_parameters


def create_or_update_parameters_in_db(
    connection: ConnectionModel,
    parameters: Dict[str, int],
    direction: Optional[str],
    current_parameters=Dict[str, Dict[str, int]],
) -> Dict[str, Dict[str, int]]:
    """
    Creates and updates parameters in the database.

    Args:
        connection: Connection object on which the updates should be made.
        parameters: Parameters which should be updated.
        direction: Direction on which the parameter should be applied (bidirectional if None)
        current_parameters: Current parameters which should be updated.

    Returns:
        Returns the current_parameters which are set in the database.
    """
    for direction in [INCOMING, OUTGOING] if direction is None else [direction]:
        for parameter_name in PARAMETERS:
            if parameter_name in parameters:
                _set_specific_parameter(
                    connection,
                    parameter_name,
                    parameters,
                    current_parameters,
                    direction,
                )
    return current_parameters


def set_parameters_with_tc(
    connection: ConnectionModel,
    parameters: Dict[str, Dict[str, int]],
    direction: Optional[str],
):
    """
    Set parameters on the host system on the given connection.

    Args:
        connection: Connection object on which the updates should be made.
        parameters: Parameters which should be configured.
        direction: Direction on which the parameter should be applied (bidirectional if None)

    Returns:
        None
    """
    tcutils.set_parameters(
        connection.connection_name,
        dbutils.get_physical_interface_by_logical_interface_id(
            connection.first_logical_interface_id
        ).physical_name,
        parameters,
        direction,
    )


def _delete_specific_parameter(
    connection: ConnectionModel,
    parameter_name: str,
    direction: str,
) -> None:

    dbutils.delete_parameter_on_connection_id(
        connection.connection_id, parameter_name, direction
    )


def delete_parameters_in_db(
    parameters: Dict[str, int],
    current_parameters: Dict[str, Dict[str, int]],
    connection: ConnectionModel,
    direction: Optional[str],
) -> Dict[str, Dict[str, int]]:
    """
    Delete specific parameters in db.

    Args:
        parameters: Parameters which should be deleted.
        current_parameters: The current parameters of the connection.
        connection: Connection object on which the updates should be made.
        direction: Direction on which the parameter should be applied (bidirectional if None)

    Returns:
        Returns the current parameters in the database.
    """

    for direction in [INCOMING, OUTGOING] if direction is None else [direction]:
        for parameter_name in PARAMETERS:
            if (
                parameter_name in parameters
                and parameter_name in current_parameters[direction]
            ):
                _delete_specific_parameter(connection, parameter_name, direction)
                current_parameters[direction].pop(parameter_name)
    return current_parameters
