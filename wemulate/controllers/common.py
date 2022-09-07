from typing import Dict, Optional, Tuple

import typer

from wemulate.ext import utils
from wemulate.core.database.models import (
    BANDWIDTH,
    DELAY,
    INCOMING,
    JITTER,
    OUTGOING,
    PACKET_LOSS,
    ConnectionModel,
)
from wemulate.utils.output import err_console


CONNECTION_NAME_PARAMETER = typer.Option(..., "--connection-name", "-n")
CONNECTION_NAME_ARGUMENT = typer.Argument(..., help="name of the connection")
DELAY_PARAMETER = typer.Option(None, "--delay", "-d")
JITTER_PARAMETER = typer.Option(None, "--jitter", "-j")
BANDWIDTH_PARAMTER = typer.Option(None, "--bandwidth", "-b")
PACKET_LOSS_PARAMETER = typer.Option(None, "--packet-loss", "-l")
SOURCE = typer.Option(None, "--source", "-src")
DESTINATION = typer.Option(None, "--destination", "-dst")


def validate_parameter_arguments(*args):
    if not any(args):
        err_console.print(
            "Please specifiy at least one parameter which should be applied on the connection | -b, --bandwidth [ms] | -j, --jitter [ms] | -d, --delay [ms], -l, --packet-loss [%]"
        )
        raise typer.Exit(1)


def check_if_connection_exists_in_db(connection_name: str) -> None:
    if not utils.connection_exists_in_db(connection_name):
        err_console.print(
            f"There is no connection {connection_name} please create a connection first"
        )
        raise typer.Exit(1)


def _check_source_destination_identical(source: str, destination: str) -> None:
    if source == destination:
        err_console.print(f"The source and destination can not be the same!")
        raise typer.Exit(1)


def _get_logical_interface_names(connection_name: str) -> Tuple[str, str]:
    connection: ConnectionModel = utils.get_connection_by_name(connection_name)
    return (
        connection.first_logical_interface.logical_name,
        connection.second_logical_interface.logical_name,
    )


def _check_if_source_destination_valid(
    source: str, destination: str, first_logical_name: str, second_logical_name: str
) -> None:
    if source not in (first_logical_name, second_logical_name):
        err_console.print(
            f"Please specify correct source information | -src, --source ({first_logical_name} | {second_logical_name})"
        )
        raise typer.Exit(1)
    if destination not in (first_logical_name, second_logical_name):
        err_console.print(
            f"Please specify correct destination information | -dst, --destination ({first_logical_name} | {second_logical_name})"
        )
        raise typer.Exit(1)


def _validate_source_destination(
    source: str, destination: str, connection_name: str
) -> str:
    _check_source_destination_identical(source, destination)
    first_logical_name, second_logical_name = _get_logical_interface_names(
        connection_name
    )
    _check_if_source_destination_valid(
        source, destination, first_logical_name, second_logical_name
    )
    return first_logical_name


def identify_direction(
    source: str, destination: str, connection_name: str
) -> Optional[str]:
    if source is None and destination is None:
        return
    else:
        first_logical_name = _validate_source_destination(
            source, destination, connection_name
        )
        if source == first_logical_name:
            return INCOMING
        else:
            return OUTGOING


def generate_pargs(
    delay: Optional[int],
    jitter: Optional[int],
    bandwidth: Optional[int],
    packet_loss: Optional[int],
) -> Dict[str, int]:
    parameters: Dict[str, int] = {}
    if bandwidth:
        parameters[BANDWIDTH] = bandwidth
    if delay:
        parameters[DELAY] = delay
    if jitter:
        parameters[JITTER] = jitter
    if packet_loss:
        parameters[PACKET_LOSS] = packet_loss
    return parameters
