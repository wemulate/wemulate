from typing import List, Optional

import typer
from rich.prompt import Confirm

import wemulate.ext.settings as settings
from wemulate.core.exc import WemulateMgmtInterfaceError
from wemulate.ext import utils
from wemulate.ext import settings
from wemulate.utils.output import err_console, console


app = typer.Typer(help="configure the application settings")


@app.command(help="set the management interface(s)", no_args_is_help=True)
def set(
    management_interfaces: Optional[List[str]] = typer.Option(
        [], "--management-interface", "-m"
    ),
    forcing: bool = typer.Option(False, "--force", "-f"),
):
    if management_interfaces:
        console.print("Changing the management interfaces will reset the device.")
        if not forcing:
            confirmation = Confirm.ask("Do you want to proceed")
            if not confirmation:
                err_console.print("Please confirm with y / yes")
                typer.Exit(1)
        settings.reset_mgmt_interfaces()
        try:
            for interface_name in management_interfaces:
                settings.add_mgmt_interface(interface_name)
            raise typer.Exit()
        except WemulateMgmtInterfaceError as e:
            err_console.print(e.message)
            raise typer.Exit(1)
    else:
        err_console.print("Please add at least one management interface")
        raise typer.Exit(1)
