from typing import List, Optional

import typer

import wemulate.controllers.common as common
import wemulate.ext.utils as utils
from wemulate.utils.output import err_console, console
from wemulate.core.database.setup import pre_setup_database


app = typer.Typer(help="restore connections and parameters stored in the database")


@app.command(help="restore all connections", no_args_is_help=False)
def device():
    utils.restore_device()
    console.print("successfully restored device")


@app.command(help="restore a specific connection", no_args_is_help=True)
def connection(connection_name: str = common.CONNECTION_NAME_PARAMETER):
    common.check_if_connection_exists_in_db(connection_name)
    utils.restore_connection(connection_name)
    console.print(f"successfully restored connection {connection_name}")
