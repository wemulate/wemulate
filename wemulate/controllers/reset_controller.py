from wemulate.utils.tcconfig import remove_connection, remove_parameters
from wemulate.core.database.utils import (
    connection_exists,
    delete_parameter,
    get_all_parameters_for_connection_id,
    get_connection,
    get_connection_list,
    get_physical_interface_for_logical_id,
    reset_all,
)
from cement import Controller, ex


class ResetController(Controller):
    class Meta:
        label = "reset"
        help = "reset connection or program"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="reset connection",
        arguments=[
            (
                ["-n", "--connection-name"],
                {
                    "help": "connection which should be resetted",
                    "action": "store",
                    "dest": "connection_name",
                },
            )
        ],
    )
    def connection(self):
        if not self.app.pargs.connection_name:
            self.app.log.info("please define a connection name | -n name")
            self.app.close()
        if connection_exists(self.app.pargs.connection_name):
            connection = get_connection(self.app.pargs.connection_name)
            parameters = get_all_parameters_for_connection_id(connection.connection_id)
            for param in parameters:
                delete_parameter(param)
            physical_interface_name = get_physical_interface_for_logical_id(
                connection.first_logical_interface_id
            ).physical_name
            remove_parameters(physical_interface_name)
            self.app.log.info(
                f"successfully resetted connection {self.app.pargs.connection_name}"
            )
            self.app.close()
        else:
            self.app.log.info(
                f"there is no connection {self.app.pargs.connection_name}"
            )
            self.app.close()

    @ex(
        help="deletes all parameters and connection",
    )
    def all(self):
        for conn in get_connection_list():
            physical_interface_name = get_physical_interface_for_logical_id(
                conn.first_logical_interface_id
            ).physical_name
            remove_parameters(physical_interface_name)
            remove_connection(conn.connection_name)
        reset_all()
        self.app.log.info("Device is resetted")
