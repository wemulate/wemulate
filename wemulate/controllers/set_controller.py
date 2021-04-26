from cement import Controller, ex
from wemulate.core.database.utils import (
    delete_all_parameter_on_connection,
    get_connection,
    connection_exists,
    create_or_update_parameter,
    get_physical_interface_for_logical_id,
)
from wemulate.utils.tcconfig import set_parameters


class SetController(Controller):
    class Meta:
        label = "set"
        help = "set specific parameter on connections"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="set parameters on a specific connection, all parameters will be overridden",
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
                    "help": "bandwidth parameter",
                    "action": "store",
                    "dest": "bandwidth",
                },
            ),
            (
                ["-j", "--jitter"],
                {"help": "jitter parameter", "action": "store", "dest": "jitter"},
            ),
            (
                ["-d", "--delay"],
                {"help": "delay parameter", "action": "store", "dest": "delay"},
            ),
            (
                ["-l", "--packet-loss"],
                {
                    "help": "packet loss parameter",
                    "action": "store",
                    "dest": "packet_loss",
                },
            ),
            # TODO specify parameter description (e.g in ms. in percent etc.)
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
                "please specifiy at least one parameter to set on the connection"
            )
            self.app.close()
        if connection_exists(self.app.pargs.connection_name):
            connection = get_connection(self.app.pargs.connection_name)
            delete_all_parameter_on_connection(connection.connection_id)
            parameters = {}
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
                f"successfully set parameters to connection {self.app.pargs.connection_name}"
            )

        else:
            self.app.log.info(
                f"there is no connection {self.app.pargs.connection_name} please create one first"
            )
            self.app.close()
