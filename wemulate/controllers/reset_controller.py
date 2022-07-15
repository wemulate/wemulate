import typer
import wemulate.controllers.common as common
from wemulate.ext import utils

app = typer.Typer(help="reset connection or the whole application settings")


@app.command(
    help="delete all parameters on a specific connection", no_args_is_help=True
)
def connection(connection_name: str = common.CONNECTION_NAME_ARGUMENT):
    common.check_if_connection_exists_in_db(connection_name)
    utils.reset_connection(connection_name)
    typer.echo(f"Successfully resetted connection {connection_name}")


@app.command(help="deletes all parameters and connection on the device")
def device():
    utils.reset_device()
    typer.echo("Successfully resetted device")
