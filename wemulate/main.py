from typing import Optional
from wemulate.core.exc import WEmulateError
from wemulate.ext.settings import check_if_mgmt_interface_set
from wemulate.core.version import get_version
from wemulate.core.database.setup import pre_setup_database
from wemulate.controllers.add_controller import app as add_app
from wemulate.controllers.set_controller import app as set_app
from wemulate.controllers.config_controller import app as config_app
from wemulate.controllers.show_controller import app as show_app
from wemulate.controllers.delete_controller import app as delete_app
from wemulate.controllers.reset_controller import app as reset_app
import os
import typer

app = typer.Typer(
    help="A modern WAN emulator",
)
app.add_typer(add_app, name="add", no_args_is_help=True)
app.add_typer(set_app, name="set", no_args_is_help=True)
app.add_typer(config_app, name="config", no_args_is_help=True)
app.add_typer(show_app, name="show", no_args_is_help=True)
app.add_typer(delete_app, name="delete", no_args_is_help=True)
app.add_typer(reset_app, name="reset", no_args_is_help=True)


def _get_version(value: bool) -> Optional[str]:
    if value:
        typer.echo(f"The current wemulate version is: {get_version()}")
        raise typer.Exit()


@app.callback(no_args_is_help=True)
def check_permissions(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_get_version,
        is_eager=True,
        help="Show program's version number and exit",
    ),
):
    if ctx.resilient_parsing:  # is used that autocompletion works
        return
    if os.getuid() == 0:
        try:
            if ctx.invoked_subcommand == "":
                ctx.invoked_subcommand = "help"
            if ctx.invoked_subcommand != "config":
                pre_setup_database()
                check_if_mgmt_interface_set()
        except WEmulateError as e:
            typer.echo(e)
            raise typer.Exit()
    else:
        typer.echo("Please start as root user")
        raise typer.Exit()


if __name__ == "__main__":
    app()
