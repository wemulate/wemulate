import wemulate.controllers.common as common
import wemulate.ext.utils as utils
from cement import Controller, ex


class ResetController(Controller):
    class Meta:
        label = "reset"
        help = "reset connection or whole application settings"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="delete all parameters on a specific connection",
        arguments=[common.CONNECTION_NAME_ARGUMENT],
    )
    def connection(self):
        if not common.connection_name_is_set(
            self
        ) or not common.connection_exists_in_db(self):
            self.app.close()
        else:
            utils.reset_connection(self.app.pargs.connection_name)
            self.app.log.info(
                f"Successfully resetted connection {self.app.pargs.connection_name}"
            )
            self.app.close()

    @ex(
        help="deletes all parameters and connection on the device",
    )
    def device(self):
        utils.reset_device()
        self.app.log.info("Successfully resetted device")
