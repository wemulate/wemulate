from wemulate.core.database.utils import (
    connection_exists,
    get_connection,
    get_connection_list,
)
from cement import Controller, ex
from wemulate.utils.rendering import rendering
import netifaces

from wemulate.utils.settings import get_interfaces, get_mgmt_interfaces, get_config_path
from wemulate.core.database.utils import get_logical_interface_for_physical_name


class ShowController(Controller):
    class Meta:
        label = "show"
        help = "show specific informations"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="show specific connection information",
        arguments=[(["connection_name"], {"help": "name of the connection"})],
    )
    def connection(self):
        headers = [
            "NAME",
            "BIDIRECTIONAL",
            "1. INTERFACE",
            "2. INTERFACE",
            "PARAMETERS",
        ]
        data = []
        if connection_exists(self.app.pargs.connection_name):
            connection = get_connection(self.app.pargs.connection_name)
            parameters = {"parameters": connection.parameters}
            parameter_string = rendering(parameters, "show_connection.jinja2")
            data.append(
                [
                    connection.connection_name,
                    connection.bidirectional,
                    connection.first_logical_interface.logical_name,
                    connection.second_logical_interface.logical_name,
                    parameter_string,
                ]
            )
            self.app.render(data, headers=headers, tablefmt="grid")
        else:
            self.app.log.info(
                f"There is no connection with name: {self.app.pargs.connection_name}"
            )

    @ex(
        help="show overview about all connections",
    )
    def connections(self):
        headers = [
            "NAME",
            "BIDIRECTIONAL",
            "1. INTERFACE",
            "2. INTERFACE",
            "PARAMETERS",
        ]
        data = []
        connections = get_connection_list()
        if connections:
            for conn in connections:
                parameters = {"parameters": conn.parameters}
                parameter_string = rendering(parameters, "show_connection.jinja2")
                data.append(
                    [
                        conn.connection_name,
                        conn.bidirectional,
                        conn.first_logical_interface.logical_name,
                        conn.second_logical_interface.logical_name,
                        parameter_string,
                    ]
                )
            self.app.render(data, headers=headers, tablefmt="grid")
        else:
            self.app.log.info("There are no connections")

    @ex(
        help="show specific interface information",
        arguments=[(["interface_name"], {"help": "name of the interface"})],
    )
    def interface(self):
        headers = ["NAME", "PHYSICAL", "IP", "MAC"]
        data = []
        if self.app.pargs.interface_name in get_interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(
                self.app.pargs.interface_name
            ):
                ip = netifaces.ifaddresses(self.app.pargs.interface_name)[
                    netifaces.AF_INET
                ][0]["addr"]
            else:
                ip = "N/A"
            data.append(
                [
                    get_logical_interface_for_physical_name(
                        self.app.pargs.interface_name
                    ).logical_name,
                    self.app.pargs.interface_name,
                    ip,
                    netifaces.ifaddresses(self.app.pargs.interface_name)[
                        netifaces.AF_LINK
                    ][0]["addr"],
                ]
            )
            self.app.render(data, headers=headers, tablefmt="grid")
        else:
            self.app.log.info("The given interface is not available")

    @ex(
        help="show overview about all interfaces",
    )
    def interfaces(self):
        headers = ["NAME", "PHYSICAL", "IP", "MAC"]
        data = []

        for int in get_interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(int):
                ip = netifaces.ifaddresses(int)[netifaces.AF_INET][0]["addr"]
            else:
                ip = "N/A"

            data.append(
                [
                    get_logical_interface_for_physical_name(int).logical_name,
                    int,
                    ip,
                    netifaces.ifaddresses(int)[netifaces.AF_LINK][0]["addr"],
                ]
            )

        self.app.render(data, headers=headers, tablefmt="grid")

    @ex(
        help="show overview about all management interfaces",
    )
    def mgmt_interfaces(self):
        headers = ["NAME", "IP", "MAC"]
        data = []
        mgmt_interfaces = get_mgmt_interfaces()
        if mgmt_interfaces == None:
            self.app.log.info(
                "There are no mgmt interfaces defined in %s" % get_config_path()
            )
        else:
            for int in get_mgmt_interfaces():
                if netifaces.AF_INET in netifaces.ifaddresses(int):
                    ip = netifaces.ifaddresses(int)[netifaces.AF_INET][0]["addr"]
                else:
                    ip = "N/A"

                data.append(
                    [
                        int,
                        ip,
                        netifaces.ifaddresses(int)[netifaces.AF_LINK][0]["addr"],
                    ]
                )

            self.app.render(data, headers=headers, tablefmt="grid")
