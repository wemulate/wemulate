import typer
from wemulate.ext import utils
from wemulate.core.database.models import BANDWIDTH, DELAY, JITTER, PACKET_LOSS
from typing import Dict, Optional


CONNECTION_NAME_PARAMETER = typer.Option(..., "--connection-name", "-n")
DELAY_PARAMETER = typer.Option(None, "--delay", "-d")
JITTER_PARAMETER = typer.Option(None, "--jitter", "-j")
BANDWIDTH_PARAMTER = typer.Option(None, "--bandwidth", "-b")
PACKET_LOSS_PARAMETER = typer.Option(None, "--packet-loss", "-l")
# BANDWIDTH_PARAMETER = ["-b", "--bandwidth"]
# BANDWIDTH_HELP_DESCRIPTION = "delete bandwidth parameter"
# JITTER_PARAMETER = ["-j", "--jitter"]
# JITTER_HELP_DESCRIPTION = "delete jitter parameter"
# DELAY_PARAMETER = ["-d", "--delay"]
# DELAY_HELP_DESCRIPTION = "delete delay parameter"
# PACKET_LOSS_PARAMETER = ["-l", "--packet-loss"]
# PACKET_LOSS_HELP_DESCRIPTION = "delete packet loss parameter"

# PARAMETER_ARGUMENT_MAP = {
#     "BANDWIDTH_STORE": (
#         BANDWIDTH_PARAMETER,
#         {"help": BANDWIDTH_HELP_DESCRIPTION, "action": "store"},
#     ),
#     "BANDWIDTH_STORE_TRUE": (
#         BANDWIDTH_PARAMETER,
#         {"help": BANDWIDTH_HELP_DESCRIPTION, "action": "store_true"},
#     ),
#     "DELAY_STORE": (
#         DELAY_PARAMETER,
#         {"help": DELAY_PARAMETER, "action": "store"},
#     ),
#     "DELAY_STORE_TRUE": (
#         DELAY_PARAMETER,
#         {"help": DELAY_PARAMETER, "action": "store_true"},
#     ),
#     "JITTER_STORE": (
#         JITTER_PARAMETER,
#         {"help": JITTER_HELP_DESCRIPTION, "action": "store"},
#     ),
#     "JITTER_STORE_TRUE": (
#         JITTER_PARAMETER,
#         {"help": JITTER_HELP_DESCRIPTION, "action": "store_true"},
#     ),
#     "PACKET_LOSS_STORE": (
#         PACKET_LOSS_PARAMETER,
#         {"help": PACKET_LOSS_HELP_DESCRIPTION, "action": "store"},
#     ),
#     "PACKET_LOSS_STORE_TRUE": (
#         PACKET_LOSS_PARAMETER,
#         {"help": PACKET_LOSS_HELP_DESCRIPTION, "action": "store_true"},
#     ),
# }


# def connection_name_is_set(obj) -> bool:
#     if not obj.app.pargs.connection_name:
#         obj.app.log.info("Please define a connection name | -n connectionname")
#         return False
#     return True


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
