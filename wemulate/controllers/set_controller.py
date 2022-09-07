from typing import Optional

import typer

import wemulate.ext.utils as utils
import wemulate.controllers.common as common
from wemulate.core.exc import WEmulateDatabaseError, WEmulateExecutionError
from wemulate.utils.output import err_console, console


app = typer.Typer(help="set parameters on a connection")


@app.command(
    help="set parameter on a specific connection, previously added parameters will be overriden",
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
        utils.set_parameter(
            connection_name,
            common.generate_pargs(delay, jitter, bandwidth, packet_loss),
            direction,
        )
        console.print(f"successfully set parameters to connection {connection_name}")
        raise typer.Exit()
    except WEmulateDatabaseError as e:
        err_console.print(e.message)
        raise typer.Exit(1)
    except WEmulateExecutionError as e:
        err_console.print(e.message)
        raise typer.Exit(1)
