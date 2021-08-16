from typing import List, Optional, Tuple
from wemulate.core.database.models import PARAMETERS
from wemulate.utils.tcconfig import add_connection, set_parameters
from wemulate.core.exc import WEmulateExecutionError, WEmulateValidationError
from wemulate.core.database.utils import (
    connection_exists,
    create_connection,
    create_or_update_parameter,
    get_connection,
    get_logical_interface_by_name,
    get_active_profile,
    get_device,
    get_physical_interface_for_logical_name,
    get_physical_interface_for_logical_id,
    get_specific_parameter_value_for_connection_id,
)
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
        physical_interface1_name: str = get_physical_interface_for_logical_name(
            logical_interfaces[0]
        ).physical_name
        physical_interface2_name: str = get_physical_interface_for_logical_name(
            logical_interfaces[1]
        ).physical_name
        return physical_interface1_name, physical_interface2_name

    def _connection_name_is_set(self) -> bool:
        if not self.app.pargs.connection_name:
            self.app.log.info("Please define a connection name | -n name")
            return False
        return True
    
    def _validate_connection_arguments(self) -> Optional[List[str]]:
        if not self._connection_name_is_set():
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

    def _validate_parameter_arguments(self) -> bool:
        if not self._connection_name_is_set():
            return False
        if (
            not self.app.pargs.bandwidth
            and not self.app.pargs.jitter
            and not self.app.pargs.delay
            and not self.app.pargs.packet_loss
        ):
            self.app.log.info(
                "Please specifiy at least one parameter which should be applied on the connection"
            )
            return False

    def _connection_exists(self) -> bool:
        if not connection_exists(self.app.pargs.connection_name):
            self.app.log.info(
                f"There is no connection {self.app.pargs.connection_name} please create a connection first"
            )
            return False
        return True 

    def _add_connection_on_host(
        self, physical_interface1_name, physical_interface2_name
    ) -> None:
        add_connection(
            self.app.pargs.connection_name,
            physical_interface1_name,
            physical_interface2_name,
        )

    def _create_connection_in_database(self, logical_interfaces: List[str]) -> None:
        create_connection(
            self.app.pargs.connection_name,
            get_logical_interface_by_name(logical_interfaces[0]),
            get_logical_interface_by_name(logical_interfaces[1]),
            get_active_profile(get_device(1)),
        )

    @ex(
        help="add a new connection",
        arguments=[
            (
                ["-n", "--connection-name"],
                {
                    "help": "name of the connection which should be created",
                    "action": "store",
                    "dest": "connection_name",
                },
            ),
            (
                ["-i", "--interfaces"],
                {
                    "help": "list of two interfaces which should be added to the connection (LAN-A,LAN-B)",
                    "action": "store",
                    "dest": "interfaces_list",
                },
            ),
        ],
    )
    def connection(self):
        logical_interfaces: Optional[
            List[str]
        ] = self._validate_connection_arguments()
        if not logical_interfaces:
            self.app.close()
        else:
            try:
                (
                    physical_interface1_name,
                    physical_interface2_name,
                ) = self._get_physical_interface_names(logical_interfaces)
                self._add_connection_on_host(
                    physical_interface1_name, physical_interface2_name
                )
                self._create_connection_in_database(logical_interfaces)
                self.app.log.info("Successfully added a new connection")
            except WEmulateValidationError as e:
                self.app.log.error(f"The {e} already exists in a connection")
            except WEmulateExecutionError as e:
                self.app.log.error("There was an execution error")

    @ex(
        help="add parameter on a specific connection, previously added parameters will not be changed",
        arguments=[
            (
                ["-n", "--connection-name"],
                {
                    "help": "name of the connection on which the parameters should be applied",
                    "action": "store",
                    "dest": "connection_name",
                },
            ),
            (
                ["-b", "--bandwidth"],
                {
                    "help": "bandwidth parameter [mbps]",
                    "action": "store",
                    "dest": "bandwidth",
                },
            ),
            (
                ["-j", "--jitter"],
                {"help": "jitter parameter [ms]", "action": "store", "dest": "jitter"},
            ),
            (
                ["-d", "--delay"],
                {"help": "delay parameter [ms]", "action": "store", "dest": "delay"},
            ),
            (
                ["-l", "--packet-loss"],
                {
                    "help": "packet loss parameter [%]",
                    "action": "store",
                    "dest": "packet_loss",
                },
            ),
        ],
    )
    def parameter(self):
        if not self._validate_connection_arguments() or not self._connection_exists(self.app.pargs.connection_name):
            self.app.close()
        else:   
            #@TODO refactor the method for better readability and strucutre
            connection = get_connection(self.app.pargs.connection_name)
                parameters = {}
                for param in PARAMETERS:
                    parameter_value = get_specific_parameter_value_for_connection_id(
                        connection.connection_id, param
                    )
                    if parameter_value:
                        parameters[param] = parameter_value
                if self.app.pargs.bandwidth:
                    parameters["bandwidth"] = self.app.pargs.bandwidth
                    create_or_update_parameter(
                        connection.connection_id, "bandwidth", self.app.pargs.bandwidth
                    )
                if self.app.pargs.jitter:
                    parameters["jitter"] = self.app.pargs.jitter
                    create_or_update_parameter(
                        connection.connection_id, "jitter", self.app.pargs.jitter
                    )
                if self.app.pargs.delay:
                    parameters["delay"] = self.app.pargs.delay
                    create_or_update_parameter(
                        connection.connection_id, "delay", self.app.pargs.delay
                    )
                if self.app.pargs.packet_loss:
                    parameters["packet_loss"] = self.app.pargs.packet_loss
                    create_or_update_parameter(
                        connection.connection_id, "packet_loss", self.app.pargs.packet_loss
                    )
                set_parameters(
                    get_physical_interface_for_logical_id(
                        get_connection(
                            self.app.pargs.connection_name
                        ).first_logical_interface_id
                    ).physical_name,
                    parameters,
                )
                self.app.log.info(
                    f"successfully added parameters to connection {self.app.pargs.connection_name}"
                )