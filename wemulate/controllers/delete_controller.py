from wemulate.core.database.models import DEFAULT_PARAMETERS, PARAMETERS
from wemulate.utils.tcconfig import remove_connection, remove_parameters
from wemulate.core.database.utils import (
    delete_parameter_on_connection_id,
    get_connection,
    delete_connection_by_name,
)
from cement import Controller, ex
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
from wemulate.utils.tcconfig import add_connection, set_parameters


class DeleteController(Controller):
    class Meta:
        label = "delete"
        help = "delete parameter or connection"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="delete a specific connection",
        arguments=[
            (
                ["-n", "--connection-name"],
                {
                    "help": "name of the desired connection",
                    "action": "store",
                    "dest": "connection_name",
                },
            )
        ],
    )
    def connection(self):
        if self.app.pargs.connection_name is None:
            self.app.log.error("please define a connection")
        elif get_connection(self.app.pargs.connection_name):
            remove_connection(self.app.pargs.connection_name)
            delete_connection_by_name(self.app.pargs.connection_name)
            self.app.log.info(
                f"connection {self.app.pargs.connection_name} successfully deleted"
            )
        else:
            self.app.log.info(
                f"there is no connection with name: {self.app.pargs.connection_name}"
            )

    @ex(
        help="delete a specific parameter on a connection",
        arguments=[
            (
                ["-n", "--connection-name"],
                {
                    "help": "name of the desired connection",
                    "action": "store",
                    "dest": "connection_name",
                },
            ),
            (
                ["-b", "--bandwidth"],
                {"help": "delete bandwidth parameter", "action": "store_true"},
            ),
            (
                ["-j", "--jitter"],
                {"help": "delete jitter parameter", "action": "store_true"},
            ),
            (
                ["-d", "--delay"],
                {"help": "delete delay parameter", "action": "store_true"},
            ),
            (
                ["-l", "--packet-loss"],
                {"help": "delete packet loss parameter", "action": "store_true"},
            ),
        ],
    )
    def parameter(self):
        if not self.app.pargs.connection_name:
            self.app.log.info("please define a connection name | -n name")
            self.app.close()
        if (
            not self.app.pargs.bandwidth
            and not self.app.pargs.jitter
            and not self.app.pargs.delay
            and not self.app.pargs.packet_loss
        ):
            self.app.log.info(
                "please specifiy at least one parameter to delete on the connection"
            )
            self.app.close()
        if connection_exists(self.app.pargs.connection_name):
            connection = get_connection(self.app.pargs.connection_name)
            parameters = {}
            for param in PARAMETERS:
                parameter_value = get_specific_parameter_value_for_connection_id(
                    connection.connection_id, param
                )
                if parameter_value:
                    parameters[param] = parameter_value

            if not parameters:
                self.app.log.info("there are no parameters set on this connection")
                self.app.close()

            if self.app.pargs.bandwidth:
                parameters.pop("bandwidth")
                delete_parameter_on_connection_id(
                    connection.connection_id,
                    "bandwidth",
                )
            if self.app.pargs.jitter:
                parameters.pop("jitter")
                delete_parameter_on_connection_id(connection.connection_id, "jitter")
            if self.app.pargs.delay:
                parameters.pop("delay")
                delete_parameter_on_connection_id(connection.connection_id, "delay")
            if self.app.pargs.packet_loss:
                parameters.pop("packet_loss")
                delete_parameter_on_connection_id(
                    connection.connection_id,
                    "packet_loss",
                )
            self.app.log.info(
                f"successfully deleted parameter on connection {self.app.pargs.connection_name}"
            )

            physical_interface_name = get_physical_interface_for_logical_id(
                get_connection(
                    self.app.pargs.connection_name
                ).first_logical_interface_id
            ).physical_name

            remove_parameters(physical_interface_name)
            set_parameters(
                physical_interface_name,
                parameters,
            )
        else:
            self.app.log.info(
                f"there is no connection {self.app.pargs.connection_name} please create one first"
            )
            self.app.close()
