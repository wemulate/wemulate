from wemulate.utils.tcconfig import remove_connection
from wemulate.core.database.utils import get_connection, delete_connection_by_name
from cement import Controller, ex


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
            self.app.log.error("Please define a connection")
        elif get_connection(self.app.pargs.connection_name):
            remove_connection(self.app.pargs.connection_name)
            delete_connection_by_name(self.app.pargs.connection_name)
            self.app.log.info(
                f"Connection {self.app.pargs.connection_name} successfully deleted"
            )
        else:
            self.app.log.info(
                f"There is no connection with name: {self.app.pargs.connection_name}"
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
        if self.app.pargs.connection_name is not None:
            self.app.log.error("test")
