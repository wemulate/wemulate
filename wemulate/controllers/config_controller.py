import typer
import wemulate.ext.settings as settings
from typing import List, Optional
from wemulate.core.exc import WemulateMgmtInterfaceError

app = typer.Typer(help="configure the application settings")


@app.command(help="set the management interface(s)")
def set(
    management_interfaces: Optional[List[str]] = typer.Option(
        [], "--management-interface", "-m"
    ),
):
    if management_interfaces:
        try:
            for interface_name in management_interfaces:
                settings.add_mgmt_interface(interface_name)
        except WemulateMgmtInterfaceError as e:
            typer.echo(e.message)
            raise typer.Exit()
    else:
        typer.echo("Please add at least one management interface")
