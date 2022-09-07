from typing import List, Optional, Tuple

import typer

import wemulate.controllers.common as common
import wemulate.ext.utils as utils
from wemulate.core.exc import (
    WEmulateDatabaseError,
    WEmulateExecutionError,
    WEmulateValidationError,
)
from wemulate.core.database.models import (
    ConnectionModel,
    LogicalInterfaceModel,
)
from wemulate.utils.output import err_console, console


def _check_if_interface_names_provided(
    first_logical_interface: str, second_logical_interface: str
) -> None:
    if not first_logical_interface or not second_logical_interface:
        err_console.print("Please define the logical interfaces | -i LAN-A LAN-B")
        raise typer.Exit(1)


def _get_logical_interface_id(logical_interface_name: str) -> int:
    logical_interface: Optional[
        LogicalInterfaceModel
    ] = utils.get_logical_interface_by_name(logical_interface_name)
    if logical_interface is not None:
        return logical_interface.logical_interface_id
    else:
        err_console.print(f"{logical_interface_name} was not found in the database!")
        raise typer.Exit(1)


def _check_if_logical_interfaces_already_used(
    first_logical_interface_name: str, second_logical_interface_name: str
) -> None:
    connections: Optional[List[ConnectionModel]] = utils.get_connection_list()
    if connections is None:
        return
    else:
        first_logical_interface_id: int = _get_logical_interface_id(
            first_logical_interface_name
        )
        second_logical_interface_id: int = _get_logical_interface_id(
            second_logical_interface_name
        )
    for conn in connections:
        if (
            conn.first_logical_interface_id == first_logical_interface_id
            or conn.first_logical_interface_id == second_logical_interface_id
            or conn.second_logical_interface_id == first_logical_interface_id
            or conn.second_logical_interface_id == second_logical_interface_id
        ):
            err_console.print("Please use an unused logical interface name")
            raise typer.Exit(1)


def _check_if_logical_interfaces_exist(
    first_logical_interface: str, second_logical_interface: str
) -> None:
    first = utils.get_logical_interface_by_name(first_logical_interface) is None
    second = utils.get_logical_interface_by_name(second_logical_interface) is None
    if first or second:
        err_console.print(
            "The provided logical interface names are unknown!\nPlease define existing logical interface names"
        )
        raise typer.Exit(1)


def _validate_connection_arguments(
    first_logical_interface_name: str, second_logical_interface_name: str
) -> None:
    _check_if_interface_names_provided(
        first_logical_interface_name, second_logical_interface_name
    )
    _check_if_logical_interfaces_exist(
        first_logical_interface_name, second_logical_interface_name
    )
    _check_if_logical_interfaces_already_used(
        first_logical_interface_name, second_logical_interface_name
    )


app = typer.Typer(help="add a new connection or parameter")


@app.command(help="add a new connection", no_args_is_help=True)
def connection(
    connection_name: str = common.CONNECTION_NAME_PARAMETER,
    logical_interfaces: Tuple[str, str] = typer.Option(
        (None, None),
        "--interfaces",
        "-i",
        show_default=False,
        help="list of two logical interfaces which should be added to the connection (LAN-A LAN-B)",
    ),
):
    (
        first_logical_interface_name,
        second_logical_interface_name,
    ) = logical_interfaces
    _validate_connection_arguments(
        first_logical_interface_name, second_logical_interface_name
    )
    try:
        utils.add_connection(
            connection_name,
            first_logical_interface_name,
            second_logical_interface_name,
        )
        console.print("Successfully added a new connection")
        raise typer.Exit()
    except WEmulateValidationError as e:
        err_console.print(f"The {e} already exists in a connection")
        raise typer.Exit(1)
    except WEmulateDatabaseError as e:
        err_console.print(e.message)
        raise typer.Exit(1)
    except WEmulateExecutionError as e:
        err_console.print(e.message)
        raise typer.Exit(1)


@app.command(
    help="add parameter on a specific connection, previously added parameters will not be changed",
    no_args_is_help=True,
)
def parameter(
    connection_name: str = common.CONNECTION_NAME_PARAMETER,
    delay: int = common.DELAY_PARAMETER,
    jitter: int = common.JITTER_PARAMETER,
    bandwidth: int = common.BANDWIDTH_PARAMTER,
    packet_loss: int = common.PACKET_LOSS_PARAMETER,
    source: str = common.SOURCE,
    destination: str = common.DESTINATION,
):
    common.check_if_connection_exists_in_db(connection_name)
    common.validate_parameter_arguments(delay, jitter, bandwidth, packet_loss)
    direction: Optional[str] = common.identify_direction(
        source, destination, connection_name
    )
    try:
        utils.add_parameter(
            connection_name,
            common.generate_pargs(delay, jitter, bandwidth, packet_loss),
            direction,
        )
        console.print(f"successfully added parameters to connection {connection_name}")
        raise typer.Exit()
    except WEmulateDatabaseError as e:
        err_console.print(e.message)
        raise typer.Exit(1)
    except WEmulateExecutionError as e:
        err_console.print(e.message)
        raise typer.Exit(1)
