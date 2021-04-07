from wemulate.core.database.models import ConnectionModel, ProfileModel
from cement import Controller, ex
import netifaces

from wemulate.utils.settings import get_interfaces, get_mgmt_interfaces, get_config_path
from wemulate.core.database import session


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
        connection = (
            session.query(ConnectionModel)
            .filter(ConnectionModel.connection_name == self.app.pargs.connection_name)
            .all()
        )
        if not connection:
            self.app.log.info("There are no connections")
        else:
            data.append(
                [
                    connection[0].connection_name,
                    connection[0].bidirectional,
                    connection[0].first_logical_interface.logical_name,
                    connection[0].second_logical_interface.logical_name,
                    connection[0].parameters,
                ]
            )
            self.app.render(data, headers=headers)
        # TODO improve parameter rendering
        self.app.log.info(
            session.query(ProfileModel)
            .filter_by(profile_name="testprofile")
            .first()
            .profile_id
        )

    @ex(
        help="show overview about all connections",
    )
    def connections(self):
        self.app.log.info("all connections will be listed here")
        # TODO implement rendering like in connection above

    @ex(
        help="show specific interface information",
        arguments=[(["interface_name"], {"help": "name of the interface"})],
    )
    def interface(self):
        headers = ["NAME", "IP", "MAC"]
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
                    self.app.pargs.interface_name,
                    ip,
                    netifaces.ifaddresses(self.app.pargs.interface_name)[
                        netifaces.AF_LINK
                    ][0]["addr"],
                ]
            )
            self.app.render(data, headers=headers)
        else:
            self.app.log.info("The given interface is not available")

    @ex(
        help="show overview about all interfaces",
    )
    def interfaces(self):
        headers = ["NAME", "IP", "MAC"]
        data = []

        for int in get_interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(int):
                ip = netifaces.ifaddresses(int)[netifaces.AF_INET][0]["addr"]
            else:
                ip = "N/A"

            data.append(
                [int, ip, netifaces.ifaddresses(int)[netifaces.AF_LINK][0]["addr"]]
            )

        self.app.render(data, headers=headers)

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
                    [int, ip, netifaces.ifaddresses(int)[netifaces.AF_LINK][0]["addr"]]
                )

            self.app.render(data, headers=headers)