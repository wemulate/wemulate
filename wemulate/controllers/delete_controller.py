from typing import Dict, List, Optional

import typer

import wemulate.ext.utils as utils
import wemulate.controllers.common as common
from wemulate.core.exc import WEmulateDatabaseError, WEmulateExecutionError
from wemulate.core.database.models import ConnectionModel
from wemulate.utils.output import err_console, console


def _check_connection_parameters(connection: ConnectionModel) -> None:
    parameter: Dict[str, int] = {
        parameter.parameter_name: parameter.value for parameter in connection.parameters
    }
    if not parameter:
        err_console.print("There are no parameters set on this connection")
        raise typer.Exit(1)


app = typer.Typer(help="delete a connection or parameter")


@app.command(help="delete a specific connection", no_args_is_help=True)
def connection(connection_name: str = common.CONNECTION_NAME_ARGUMENT):
    common.check_if_connection_exists_in_db(connection_name)
    utils.delete_connection(connection_name)
    console.print(f"connection {connection_name} successfully deleted")
    raise typer.Exit()


@app.command(help="delete parameter(s) on a specific connection", no_args_is_help=True)
def parameter(
    connection_name: str = common.CONNECTION_NAME_PARAMETER,
    delay: bool = common.DELAY_PARAMETER,
    jitter: bool = common.JITTER_PARAMETER,
    bandwidth: bool = common.BANDWIDTH_PARAMTER,
    packet_loss: bool = common.PACKET_LOSS_PARAMETER,
    source: str = common.SOURCE,
    destination: str = common.DESTINATION,
):
    common.check_if_connection_exists_in_db(connection_name)
    common.validate_parameter_arguments(delay, jitter, bandwidth, packet_loss)
    direction: Optional[str] = common.identify_direction(
        source, destination, connection_name
    )
    _check_connection_parameters(utils.get_connection_by_name(connection_name))
    try:

        utils.delete_parameter(
            connection_name,
            common.generate_pargs(delay, jitter, bandwidth, packet_loss),
            direction,
        )
        console.print(f"Successfully deleted parameter on connection {connection_name}")
        raise typer.Exit()
    except WEmulateDatabaseError as e:
        err_console.print(e.message)
        raise typer.Exit(1)
    except WEmulateExecutionError as e:
        err_console.print(e.message)
        raise typer.Exit(1)
