import wemulate.ext.settings as settings
from typing import List
from cement import Controller, ex
from wemulate.core.exc import WemulateMgmtInterfaceError


class ConfigController(Controller):
    class Meta:
        label: str = "config"
        help: str = "configure the application settings"
        stacked_on: str = "base"
        stacked_type: str = "nested"

    def _get_management_interfaces(self) -> List[str]:
        return self.app.pargs.mgmt_interfaces.split(",")

    @ex(
        help="set the management interface(s)",
        arguments=[
            (
                ["-m", "--management-interface"],
                {
                    "help": "comma-separated list of interfaces, which should be set as management interface(s)",
                    "action": "store",
                    "dest": "mgmt_interfaces",
                },
            )
        ],
    )
    def set(self):
        if self.app.pargs.mgmt_interfaces is not None:
            try:
                mgmt_interfaces: List[str] = self._get_management_interfaces()
                for interface_name in mgmt_interfaces:
                    settings.add_mgmt_interface(interface_name)
            except WemulateMgmtInterfaceError as e:
                self.app.log.error(e.message)
        else:
            self.app.log.info("Please add at least one management interface")
            self.app.close()
