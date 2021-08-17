from typing import Dict, List, Optional, Tuple
from wemulate.core.database.models import (
    BANDWIDTH,
    ConnectionModel,
    DELAY,
    JITTER,
    PACKET_LOSS,
)
import wemulate.utils.tcconfig as tcutils
import wemulate.core.database.utils as dbutils
from wemulate.core.exc import (
    WEmulateDatabaseError,
    WEmulateExecutionError,
    WEmulateValidationError,
)
import wemulate.controllers.common as common
from cement import Controller, ex


class AddController(Controller):
    class Meta:
        label: str = "add"
        help: str = "add a new connection or parameter"
        stacked_on: str = "base"
        stacked_type: str = "nested"

    def _get_physical_interface_names(
        self, logical_interfaces: List[str]
    ) -> Tuple[str, str]:
        physical_interface1_name: str = dbutils.get_physical_interface_for_logical_name(
            logical_interfaces[0]
        ).physical_name
        physical_interface2_name: str = dbutils.get_physical_interface_for_logical_name(
            logical_interfaces[1]
        ).physical_name
        return physical_interface1_name, physical_interface2_name

    def _validate_connection_arguments(self) -> Optional[List[str]]:
        if not common.connection_name_is_set(self):
            return
        if not self.app.pargs.interfaces_list:
            self.app.log.info("Please define the logical interfaces | -i LAN-A,LAN-B")
            return
        else:
            logical_interfaces: List[str] = self.app.pargs.interfaces_list.split(",")
            if len(logical_interfaces) != 2:
                self.app.log.info(
                    "Please define exactly two interfaces | -i LAN-A,LAN-B"
                )
                return
            return logical_interfaces

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
        logical_interfaces: Optional[List[str]] = self._validate_connection_arguments()
        if not logical_interfaces:
            self.app.close()
        else:
            try:
                (
                    physical_interface1_name,
                    physical_interface2_name,
                ) = self._get_physical_interface_names(logical_interfaces)
                tcutils.add_connection(
                    self.app.pargs.connection_name,
                    physical_interface1_name,
                    physical_interface2_name,
                )
                dbutils.create_connection(
                    self.app.pargs.connection_name,
                    dbutils.get_logical_interface_by_name(logical_interfaces[0]),
                    dbutils.get_logical_interface_by_name(logical_interfaces[1]),
                    dbutils.get_active_profile(dbutils.get_device(1)),
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
            common.BANDWIDTH_ARGUMENT,
            common.DELAY_ARGUMENT,
            common.JITTER_ARGUMENT,
            common.PACKET_LOSS_ARGUMENT,
        ],
    )
    def parameter(self):
        if not common.connection_exists_in_db(
            self
        ) or not common.validate_parameter_arguments(self):
            self.app.close()
        else:
            try:
                connection: ConnectionModel = dbutils.get_connection(
                    self.app.pargs.connection_name
                )
                parameters: Dict[
                    str, int
                ] = dbutils.get_all_parameter_values_for_connection_id(
                    connection.connection_id
                )
                common.create_or_update_parameters_in_db(self, connection, parameters)
                tcutils.set_parameters(
                    dbutils.get_physical_interface_for_logical_id(
                        connection.first_logical_interface_id
                    ).physical_name,
                    parameters,
                )
                self.app.log.info(
                    f"successfully added parameters to connection {self.app.pargs.connection_name}"
                )

            except WEmulateDatabaseError as e:
                self.app.log.error(e.message)
            except WEmulateExecutionError as e:
                self.app.log.error(e.message)
