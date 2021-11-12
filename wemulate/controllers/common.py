import typer
from wemulate.ext import utils
from wemulate.core.database.models import BANDWIDTH, DELAY, JITTER, PACKET_LOSS
from typing import Dict, Optional


CONNECTION_NAME_PARAMETER = typer.Option(..., "--connection-name", "-n")
CONNECTION_NAME_ARGUMENT = typer.Argument(..., help="name of the connection")
DELAY_PARAMETER = typer.Option(None, "--delay", "-d")
JITTER_PARAMETER = typer.Option(None, "--jitter", "-j")
BANDWIDTH_PARAMTER = typer.Option(None, "--bandwidth", "-b")
PACKET_LOSS_PARAMETER = typer.Option(None, "--packet-loss", "-l")


def validate_parameter_arguments(*args):
    if not any(args):
        typer.echo(
            "Please specifiy at least one parameter which should be applied on the connection | -b, --bandwidth [ms] | -j, --jitter [ms] | -d, --delay [ms], -l, --packet-loss [%]"
        )
        raise typer.Exit()


def check_if_connection_exists_in_db(connection_name: str):
    if not utils.connection_exists_in_db(connection_name):
        typer.echo(
            f"There is no connection {connection_name} please create a connection first"
        )
        raise typer.Exit()


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
