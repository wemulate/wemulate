import tabulate
import typer
import wemulate.controllers.common as common
import wemulate.ext.utils as utils
import wemulate.ext.settings as settings
from typing import List
from wemulate.core.database.models import ConnectionModel, ParameterModel
from wemulate.utils.rendering import rendering

CONNECTION_HEADERS: List[str] = [
    "NAME",
    "1. INTERFACE",
    "2. INTERFACE",
    "PARAMETERS",
]
SHOW_CONNECTION_TEMPLATE_FILE: str = "show_connection.jinja2"
INTERFACE_HEADER = ["NAME", "PHYSICAL", "IP", "MAC"]


def _get_parameters_to_render(parameters: List[ParameterModel]) -> List[ParameterModel]:
    parameters_to_render: List[ParameterModel] = parameters.copy()
    for i, current_parameter in enumerate(parameters):
        for parameter_to_check in parameters[i + 1 :]:
            if (
                parameter_to_check.parameter_name == current_parameter.parameter_name
                and parameter_to_check.value == current_parameter.value
            ):
                parameters_to_render[
                    parameters_to_render.index(current_parameter)
                ].direction = None
                parameters_to_render.remove(parameter_to_check)
                break
    return parameters_to_render


def _construct_connection_data_to_render(
    connection: ConnectionModel, render_data: List
) -> None:
    parameters: List[ParameterModel] = _get_parameters_to_render(connection.parameters)
    render_data.append(
        [
            connection.connection_name,
            connection.first_logical_interface.logical_name,
            connection.second_logical_interface.logical_name,
            rendering(
                {"parameters": parameters},
                SHOW_CONNECTION_TEMPLATE_FILE,
            ),
        ]
    )


def _construct_interface_data_to_render(
    render_data: List, interface: str, is_mgmt_interface: bool = False
) -> None:
    data_to_append: List = []
    if not is_mgmt_interface:
        data_to_append.append(
            utils.get_logical_interface_by_physical_name(interface).logical_name,
        )
    data_to_append.extend(
        [
            interface,
            settings.get_interface_ip(interface),
            settings.get_interface_mac_address(interface),
        ]
    )
    render_data.append(data_to_append)


app = typer.Typer(help="show specific information")


@app.command(help="show specific connection information", no_args_is_help=True)
def connection(connection_name: str = common.CONNECTION_NAME_ARGUMENT):
    common.check_if_connection_exists_in_db(connection_name)
    connection: ConnectionModel = utils.get_connection_by_name(connection_name)
    render_data: List[str] = []
    _construct_connection_data_to_render(connection, render_data)
    typer.echo(
        tabulate.tabulate(render_data, headers=CONNECTION_HEADERS, tablefmt="grid")
    )


@app.command(help="show overview about all connections")
def connections():
    connections: List[ConnectionModel] = utils.get_connection_list()
    if not connections:
        typer.echo("There are no connections")
        raise typer.Exit()
    else:
        render_data: List = []
        for connection in connections:
            _construct_connection_data_to_render(connection, render_data)
        typer.echo(
            tabulate.tabulate(render_data, headers=CONNECTION_HEADERS, tablefmt="grid")
        )


@app.command(help="show specific interface information", no_args_is_help=True)
def interface(interface_name: str = typer.Argument(..., help="name of the interface")):
    if not interface_name in settings.get_non_mgmt_interfaces():
        typer.echo("The given interface is not available")
    else:
        render_data: List = []
        _construct_interface_data_to_render(
            render_data,
            interface_name,
        )
        typer.echo(
            tabulate.tabulate(render_data, headers=INTERFACE_HEADER, tablefmt="grid")
        )


@app.command(help="show overview about all interfaces")
def interfaces():
    render_data: List = []
    for interface in settings.get_non_mgmt_interfaces():
        _construct_interface_data_to_render(render_data, interface)
    typer.echo(
        tabulate.tabulate(render_data, headers=INTERFACE_HEADER, tablefmt="grid")
    )


@app.command(help="show overview about all management interfaces")
def mgmt_interfaces():
    mgmt_interfaces: List[str] = settings.get_mgmt_interfaces()
    render_data: List = []
    for interface in mgmt_interfaces:
        _construct_interface_data_to_render(
            render_data, interface, is_mgmt_interface=True
        )
    typer.echo(
        tabulate.tabulate(render_data, headers=["NAME", "IP", "MAC"], tablefmt="grid")
    )
