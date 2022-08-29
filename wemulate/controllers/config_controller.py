import typer
import wemulate.ext.settings as settings
from typing import List, Optional
from wemulate.core.exc import WemulateMgmtInterfaceError
from wemulate.ext import utils
from wemulate.ext import settings

app = typer.Typer(help="configure the application settings")


@app.command(help="set the management interface(s)", no_args_is_help=True)
def set(
    management_interfaces: Optional[List[str]] = typer.Option(
        [], "--management-interface", "-m"
    ),
    forcing: bool = typer.Option(False, "--force", "-f"),
):
    if management_interfaces:
        typer.echo("Changing the management interfaces will reset the device.")
        if not forcing:
            confirmation = typer.prompt("Do you want to proceed (y / yes)?")
            if confirmation != "y" and confirmation != "yes":
                typer.echo("Please confirm with y / yes")
                typer.Exit()
        settings.reset_mgmt_interfaces()
        try:
            for interface_name in management_interfaces:
                settings.add_mgmt_interface(interface_name)
        except WemulateMgmtInterfaceError as e:
            typer.echo(e.message)
            raise typer.Exit()
    else:
        typer.echo("Please add at least one management interface")
