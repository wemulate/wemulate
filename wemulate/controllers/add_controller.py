import wemulate.controllers.common as common
import wemulate.ext.utils as utils
from typing import List, Optional, Tuple
from wemulate.core.exc import (
    WEmulateDatabaseError,
    WEmulateExecutionError,
    WEmulateValidationError,
)
from cement import Controller, ex
from wemulate.core.database.models import ConnectionModel, LogicalInterfaceModel


class AddController(Controller):
    class Meta:
        label: str = "add"
        help: str = "add a new connection or parameter"
        stacked_on: str = "base"
        stacked_type: str = "nested"

    def _logical_interface_used(self, logical_interface_name: str) -> bool:
        connections: Optional[List[ConnectionModel]] = utils.get_connection_list()
        logical_interface_id: Optional[
            LogicalInterfaceModel
        ] = utils.get_logical_interface_by_name(
            logical_interface_name
        ).logical_interface_id
        for conn in connections:
            if (
                conn.first_logical_interface_id == logical_interface_id
                or conn.second_logical_interface_id == logical_interface_id
            ):
                return True
        return False

    def _validate_connection_arguments(self) -> Tuple[Optional[str], Optional[str]]:
        if not common.connection_name_is_set(self):
            return None, None
        if not self.app.pargs.interfaces_list:
            self.app.log.info("Please define the logical interfaces | -i LAN-A,LAN-B")
            return None, None
        else:
            logical_interfaces: List[str] = self.app.pargs.interfaces_list.split(",")
            if len(logical_interfaces) != 2:
                self.app.log.info(
                    "Please define exactly two interfaces | -i LAN-A,LAN-B"
                )
                return None, None
            if not utils.get_logical_interface_by_name(
                logical_interfaces[0]
            ) or not utils.get_logical_interface_by_name(logical_interfaces[1]):
                self.app.log.info("Please define existing logical interface names")
                return None, None
            if self._logical_interface_used(
                logical_interfaces[0]
            ) or self._logical_interface_used(logical_interfaces[1]):
                self.app.log.info("Please use an unused logical interface name")
                return None, None
            return logical_interfaces[0], logical_interfaces[1]

    @ex(
        help="add a new connection",
        arguments=[
            common.CONNECTION_NAME_ARGUMENT,
            (
                ["-i", "--interfaces"],
                {
                    "help": "list of two logical interfaces which should be added to the connection (LAN-A,LAN-B)",
                    "action": "store",
                    "dest": "interfaces_list",
                },
            ),
        ],
    )
    def connection(self):
        (
            first_logical_interface,
            second_logical_interface,
        ) = self._validate_connection_arguments()
        if not first_logical_interface or not second_logical_interface:
            self.app.close()
        else:
            try:
                utils.add_connection(
                    self.app.pargs.connection_name,
                    first_logical_interface,
                    second_logical_interface,
                )
                self.app.log.info("Successfully added a new connection")
            except WEmulateValidationError as e:
                self.app.log.error(f"The {e} already exists in a connection")
            except WEmulateDatabaseError as e:
                self.app.log.error(e.message)
            except WEmulateExecutionError as e:
                self.app.log.error(e.message)

    @ex(
        help="add parameter on a specific connection, previously added parameters will not be changed",
        arguments=[
            common.CONNECTION_NAME_ARGUMENT,
            common.PARAMETER_ARGUMENT_MAP["DELAY_STORE"],
            common.PARAMETER_ARGUMENT_MAP["JITTER_STORE"],
            common.PARAMETER_ARGUMENT_MAP["BANDWIDTH_STORE"],
            common.PARAMETER_ARGUMENT_MAP["PACKET_LOSS_STORE"],
        ],
    )
    def parameter(self):
        if (
            not common.connection_name_is_set(self)
            or not common.connection_exists_in_db(self)
            or not common.validate_parameter_arguments(self)
        ):
            self.app.close()
        else:
            try:
                utils.add_parameter(
                    self.app.pargs.connection_name, common.generate_pargs(self)
                )
                self.app.log.info(
                    f"successfully added parameters to connection {self.app.pargs.connection_name}"
                )

            except WEmulateDatabaseError as e:
                self.app.log.error(e.message)
            except WEmulateExecutionError as e:
                self.app.log.error(e.message)
