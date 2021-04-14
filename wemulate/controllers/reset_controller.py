from wemulate.core.database.utils import (
    connection_exists,
    delete_connection_by_name,
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
        help="example sub command1",
        arguments=[
            (
                ["-n", "--connection-name"],
                {
                    "help": "notorious foo option",
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
            delete_connection_by_name(self.app.pargs.connection_name)
            self.app.log.info(
                f"successfully deleted connection {self.app.pargs.connection_name}"
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
