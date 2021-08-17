from re import I
import wemulate.core.database.utils as dbutils
from wemulate.core.database.models import (
    BANDWIDTH,
    JITTER,
    DELAY,
    PACKET_LOSS,
    ConnectionModel,
)
from typing import Dict

CONNECTION_NAME = "connection_name"
CONNECTION_NAME_ARGUMENT = (
    ["-n", "--connection-name"],
    {
        "help": "name of the desired connection",
        "action": "store",
        "dest": CONNECTION_NAME,
    },
)
BANDWIDTH_ARGUMENT = (
    ["-b", "--bandwidth"],
    {"help": "delete bandwidth parameter", "action": "store_true"},
)
JITTER_ARGUMENT = (
    ["-j", "--jitter"],
    {"help": "delete jitter parameter", "action": "store_true"},
)
DELAY_ARGUMENT = (
    ["-d", "--delay"],
    {"help": "delete delay parameter", "action": "store_true"},
)
PACKET_LOSS_ARGUMENT = (
    ["-l", "--packet-loss"],
    {"help": "delete packet loss parameter", "action": "store_true"},
)


def _set_bandwidth(
    obj, connection: ConnectionModel, parameters: Dict[str, int]
) -> None:
    if obj.app.pargs.bandwidth:
        parameters[BANDWIDTH] = obj.app.pargs.bandwidth
        dbutils.create_or_update_parameter(
            connection.connection_id, BANDWIDTH, obj.app.pargs.bandwidth
        )


def _set_jitter(obj, connection: ConnectionModel, parameters: Dict[str, int]) -> None:
    if obj.app.pargs.jitter:
        parameters[JITTER] = obj.app.pargs.jitter
        dbutils.create_or_update_parameter(
            connection.connection_id, JITTER, obj.app.pargs.jitter
        )


def _set_delay(
    obj,
    connection: ConnectionModel,
    parameters: Dict[str, int],
) -> None:
    if obj.app.pargs.delay:
        parameters[DELAY] = obj.app.pargs.delay
        dbutils.create_or_update_parameter(
            connection.connection_id, DELAY, obj.app.pargs.delay
        )


def _set_packet_loss(
    obj, connection: ConnectionModel, parameters: Dict[str, int]
) -> None:
    if obj.app.pargs.packet_loss:
        parameters[PACKET_LOSS] = obj.app.pargs.packet_loss
        dbutils.create_or_update_parameter(
            connection.connection_id, PACKET_LOSS, obj.app.pargs.packet_loss
        )


def create_or_update_parameters_in_db(
    obj, connection: ConnectionModel, parameters: Dict[str, int]
) -> None:
    _set_bandwidth(obj, connection, parameters)
    _set_jitter(obj, connection, parameters)
    _set_delay(obj, connection, parameters)
    _set_packet_loss(obj, connection, parameters)


def connection_name_is_set(obj) -> bool:
    if not obj.app.pargs.connection_name:
        obj.app.log.info("Please define a connection name | -n connectionname")
        return False
    return True


def validate_parameter_arguments(obj) -> bool:
    if not connection_name_is_set(obj):
        return False
    if (
        not obj.app.pargs.bandwidth
        and not obj.app.pargs.jitter
        and not obj.app.pargs.delay
        and not obj.app.pargs.packet_loss
    ):
        obj.app.log.info(
            "Please specifiy at least one parameter which should be applied on the connection"
        )
        return False
    return True


def connection_exists_in_db(obj) -> bool:
    if not dbutils.connection_exists(obj.app.pargs.connection_name):
        obj.app.log.info(
            f"There is no connection {obj.app.pargs.connection_name} please create a connection first"
        )
        return False
    return True
