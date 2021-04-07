from wemulate.core.database.models import ConnectionModel
from cement import Controller, ex

from wemulate.utils.settings import (
    get_interfaces,
    get_mgmt_interfaces,
    get_config_path,
)
from wemulate.core.database import session


class ListController(Controller):
    class Meta:
        label = "list"
        help = "list specific informations"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="list all connections",
    )
    def connections(self):
        headers = ["NAME", "BIDIRECTIONAL", "1. INTERFACE", "2. INTERFACE"]
        data = []
        connections = session.query(ConnectionModel).all()
        if not connections:
            self.app.log.info("There are no connections")
        else:
            for conn in connections:
                data.append(
                    [
                        conn.connection_name,
                        conn.bidirectional,
                        conn.first_logical_interface.logical_name,
                        conn.second_logical_interface.logical_name,
                    ]
                )
            self.app.render(data, headers=headers)

    @ex(
        help="list all interfaces",
    )
    def interfaces(self):
        data = {"interfaces": get_interfaces()}
        self.app.render(data, "list_interfaces.jinja2", handler="jinja2")

    @ex(
        help="list all management interfaces",
    )
    def mgmt_interfaces(self):
        mgmt_interfaces = get_mgmt_interfaces()
        if mgmt_interfaces == None:
            self.app.log.info(
                "There are no mgmt interfaces defined in %s" % get_config_path()
            )
        else:
            data = {"interfaces": mgmt_interfaces}
            self.app.render(data, "list_interfaces.jinja2", handler="jinja2")
