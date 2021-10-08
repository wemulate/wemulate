import wemulate.controllers.common as common
import wemulate.ext.utils as utils
import wemulate.ext.settings as settings
from typing import List
from wemulate.core.database.models import ConnectionModel
from cement import Controller, ex
from wemulate.utils.rendering import rendering


class ShowController(Controller):
    CONNECTION_HEADERS: List[str] = [
        "NAME",
        "BIDIRECTIONAL",
        "1. INTERFACE",
        "2. INTERFACE",
        "PARAMETERS",
    ]
    SHOW_CONNECTION_TEMPLATE_FILE: str = "show_connection.jinja2"
    INTERFACE_HEADER = ["NAME", "PHYSICAL", "IP", "MAC"]

    class Meta:
        label: str = "show"
        help: str = "show specific information"
        stacked_on: str = "base"
        stacked_type: str = "nested"

    def _construct_connection_data_to_render(
        self, connection: ConnectionModel, render_data: List
    ) -> None:
        render_data.append(
            [
                connection.connection_name,
                connection.bidirectional,
                connection.first_logical_interface.logical_name,
                connection.second_logical_interface.logical_name,
                rendering(
                    {"parameters": connection.parameters},
                    self.SHOW_CONNECTION_TEMPLATE_FILE,
                ),
            ]
        )

    def _construct_interface_data_to_render(
        self, render_data: List, interface: str, is_mgmt_interface: bool = False
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

    @ex(
        help="show specific connection information",
        arguments=[([common.CONNECTION_NAME], {"help": "name of the connection"})],
    )
    def connection(self):
        if not common.connection_exists_in_db(self):
            self.app.close()
        else:
            connection: ConnectionModel = utils.get_connection_by_name(
                self.app.pargs.connection_name
            )
            render_data: List = []
            self._construct_connection_data_to_render(connection, render_data)
            self.app.render(
                render_data, headers=self.CONNECTION_HEADERS, tablefmt="grid"
            )

    @ex(
        help="show overview about all connections",
    )
    def connections(self):
        connections: List[ConnectionModel] = utils.get_connection_list()
        if not connections:
            self.app.log.info("There are no connections")
            self.app.close()
        else:
            render_data: List = []
            for connection in connections:
                self._construct_connection_data_to_render(connection, render_data)
            self.app.render(
                render_data, headers=self.CONNECTION_HEADERS, tablefmt="grid"
            )

    @ex(
        help="show specific interface information",
        arguments=[(["interface_name"], {"help": "name of the interface"})],
    )
    def interface(self):
        if not self.app.pargs.interface_name in settings.get_interfaces():
            self.app.log.info("The given interface is not available")
        else:
            render_data: List = []
            self._construct_interface_data_to_render(
                render_data,
                self.app.pargs.interface_name,
            )
            self.app.render(render_data, headers=self.INTERFACE_HEADER, tablefmt="grid")

    @ex(
        help="show overview about all interfaces",
    )
    def interfaces(self):
        render_data: List = []
        for interface in settings.get_interfaces():
            self._construct_interface_data_to_render(render_data, interface)
        self.app.render(render_data, headers=self.INTERFACE_HEADER, tablefmt="grid")

    @ex(
        help="show overview about all management interfaces",
    )
    def mgmt_interfaces(self):
        mgmt_interfaces: List[str] = settings.get_mgmt_interfaces()
        if not mgmt_interfaces:
            self.app.log.info(
                "There are no mgmt interfaces defined in %s"
                % settings.get_config_path()
            )
            self.app.close()
        else:
            render_data: List = []
            for interface in mgmt_interfaces:
                self._construct_interface_data_to_render(render_data, interface, True)
            self.app.render(render_data, headers=["NAME", "IP", "MAC"], tablefmt="grid")
