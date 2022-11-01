from typing import List, Optional

import typer
from rich.prompt import Confirm

from wemulate.core.exc import WemulateMgmtInterfaceError
from wemulate.ext import settings
from wemulate.utils.output import err_console, console
from wemulate.core.database.setup import pre_setup_database


def _check_if_physical_interfaces_exists(management_interfaces: List[str]):
    for interface in management_interfaces:
        if not settings.check_if_interface_present_on_device(interface):
            err_console.print(
                f"The interface {interface} is not physically present on the device!"
            )
            raise typer.Exit(1)


app = typer.Typer(help="configure the application settings")


@app.command(help="set the management interface(s)", no_args_is_help=True)
def set(
    management_interfaces: Optional[List[str]] = typer.Option(
        [], "--management-interface", "-m"
    ),
    forcing: bool = typer.Option(False, "--force", "-f"),
):
    if management_interfaces:
        _check_if_physical_interfaces_exists(management_interfaces)
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
            pre_setup_database()
            raise typer.Exit()
        except WemulateMgmtInterfaceError as e:
            err_console.print(e.message)
            raise typer.Exit(1)
    else:
        err_console.print("Please add at least one management interface")
        raise typer.Exit(1)
