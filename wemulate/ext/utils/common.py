import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils
from typing import Dict
from wemulate.core.database.models import (
    BANDWIDTH,
    JITTER,
    DELAY,
    PACKET_LOSS,
    ConnectionModel,
)


def _set_bandwidth(
    connection: ConnectionModel,
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
) -> None:
    if BANDWIDTH in parameters:
        current_parameters[BANDWIDTH] = parameters[BANDWIDTH]
        dbutils.create_or_update_parameter(
            connection.connection_id, BANDWIDTH, parameters[BANDWIDTH]
        )


def _set_jitter(
    connection: ConnectionModel,
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
) -> None:
    if JITTER in parameters:
        current_parameters[JITTER] = parameters[JITTER]
        dbutils.create_or_update_parameter(
            connection.connection_id, JITTER, parameters[JITTER]
        )


def _set_delay(
    connection: ConnectionModel,
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
) -> None:
    if DELAY in parameters:
        current_parameters[DELAY] = parameters[DELAY]
        dbutils.create_or_update_parameter(
            connection.connection_id, DELAY, parameters[DELAY]
        )


def _set_packet_loss(
    connection: ConnectionModel,
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
) -> None:
    if PACKET_LOSS in parameters:
        current_parameters[PACKET_LOSS] = parameters[PACKET_LOSS]
        dbutils.create_or_update_parameter(
            connection.connection_id, PACKET_LOSS, parameters[PACKET_LOSS]
        )


def create_or_update_parameters_in_db(
    connection: ConnectionModel,
    parameters: Dict[str, int],
    current_parameters={},
) -> Dict[str, int]:
    """
    Creates and updates parameters in the database.

    Args:
        connection: Connection object on which the updates should be made.
        parameters: Parameters which should be updated.
        current_parameters: Current parameters which should be updated.

    Returns:
        Returns the current_parameters which are set in the database.
    """
    _set_bandwidth(connection, parameters, current_parameters)
    _set_jitter(connection, parameters, current_parameters)
    _set_delay(connection, parameters, current_parameters)
    _set_packet_loss(connection, parameters, current_parameters)
    return current_parameters


def set_parameters_with_tc(connection: ConnectionModel, parameters: Dict[str, int]):
    """
    Set parameters on the host system on the given connection.

    Args:
        connection: Connection object on which the updates should be made.
        parameters: Parameters which should be configured.

    Returns:
        None
    """
    tcutils.set_parameters(
        connection.connection_name,
        dbutils.get_physical_interface_by_logical_interface_id(
            connection.first_logical_interface_id
        ).physical_name,
        parameters,
    )


def _delete_bandwidth(
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
    connection: ConnectionModel,
) -> None:
    if BANDWIDTH in parameters:
        current_parameters.pop(BANDWIDTH)
        dbutils.delete_parameter_on_connection_id(
            connection.connection_id,
            BANDWIDTH,
        )


def _delete_jitter(
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
    connection: ConnectionModel,
) -> None:
    if JITTER in parameters:
        current_parameters.pop(JITTER)
        dbutils.delete_parameter_on_connection_id(connection.connection_id, JITTER)


def _delete_delay(
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
    connection: ConnectionModel,
) -> None:
    if DELAY in parameters:
        current_parameters.pop(DELAY)
        dbutils.delete_parameter_on_connection_id(connection.connection_id, DELAY)


def _delete_packet_loss(
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
    connection: ConnectionModel,
) -> None:
    if PACKET_LOSS in parameters:
        current_parameters.pop(PACKET_LOSS)
        dbutils.delete_parameter_on_connection_id(
            connection.connection_id,
            PACKET_LOSS,
        )


def delete_parameters_in_db(
    parameters: Dict[str, int],
    current_parameters: Dict[str, int],
    connection: ConnectionModel,
) -> Dict[str, int]:
    """
    Delete specific parameters in db.

    Args:
        parameters: Parameters which should be deleted.
        current_parameters: The current parameters on the connection.
        connection: Connection object on which the updates should be made.

    Returns:
        Returns the current parameters in the database.
    """
    _delete_bandwidth(parameters, current_parameters, connection)
    _delete_jitter(parameters, current_parameters, connection)
    _delete_delay(parameters, current_parameters, connection)
    _delete_packet_loss(parameters, current_parameters, connection)
    return current_parameters
