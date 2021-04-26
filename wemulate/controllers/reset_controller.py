from wemulate.utils.tcconfig import remove_parameters
from wemulate.core.database.utils import (
    connection_exists,
    delete_connection_by_name,
    get_connection,
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

            remove_parameters(
                get_physical_interface_for_logical_id(
                    get_connection(
                        self.app.pargs.connection_name
                    ).first_logical_interface_id
                ).physical_name
            )
            self.app.log.info(
                f"successfully resetted connection {self.app.pargs.connection_name}"
            )
            self.app.close()
            # TODO delete connection physically
        else:
            self.app.log.info(
                f"there is no connection {self.app.pargs.connection_name}"
            )
            self.app.close()

    @ex(
        help="example sub command1",
    )
    def all(self):
        reset_all()
        self.app.log.info("Device is resetted")
        # TODO reset device physically
