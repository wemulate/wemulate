import typer
import wemulate.ext.settings as settings
from typing import List, Optional
from wemulate.core.exc import WemulateMgmtInterfaceError
from wemulate.ext import utils

app = typer.Typer(help="configure the application settings")


@app.command(help="set the management interface(s)", no_args_is_help=True)
def set(
    management_interfaces: Optional[List[str]] = typer.Option(
        [], "--management-interface", "-m"
    ),
):
    if management_interfaces:
        typer.echo("Changing the management interfaces will reset the device.")
        confirmation = typer.prompt("Do you want to proceed (y / yes)?")
        if confirmation == "y" or confirmation == "yes":
            utils.reset_device()
            try:
                for interface_name in management_interfaces:
                    settings.add_mgmt_interface(interface_name)
            except WemulateMgmtInterfaceError as e:
                typer.echo(e.message)
                raise typer.Exit()
        else:
            typer.echo("Please confirm with y / yes")
            typer.Exit()
    else:
        typer.echo("Please add at least one management interface")
