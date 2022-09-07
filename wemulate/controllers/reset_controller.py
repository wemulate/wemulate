import typer

import wemulate.controllers.common as common
from wemulate.ext import utils
from wemulate.utils.output import console


app = typer.Typer(help="reset connection or the whole application settings")


@app.command(
    help="delete all parameters on a specific connection", no_args_is_help=True
)
def connection(connection_name: str = common.CONNECTION_NAME_ARGUMENT):
    common.check_if_connection_exists_in_db(connection_name)
    utils.reset_connection(connection_name)
    console.print(f"Successfully resetted connection {connection_name}")
    raise typer.Exit()


@app.command(help="deletes all parameters and connection on the device")
def device():
    utils.reset_device()
    console.print("Successfully resetted device")
    raise typer.Exit()
