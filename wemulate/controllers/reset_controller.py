import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils
import wemulate.controllers.common as common
from cement import Controller, ex
from wemulate.core.database.models import ConnectionModel


class ResetController(Controller):
    class Meta:
        label = "reset"
        help = "reset connection or whole application settings"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="reset connection",
        arguments=[common.CONNECTION_NAME_ARGUMENT],
    )
    def connection(self):
        if not common.connection_name_is_set(
            self
        ) or not common.connection_exists_in_db(self):
            self.app.close()
        else:
            connection: ConnectionModel = dbutils.get_connection(
                self.app.pargs.connection_name
            )
            dbutils.delete_all_parameter_on_connection(connection.connection_id)
            physical_interface_name = dbutils.get_physical_interface_for_logical_id(
                connection.first_logical_interface_id
            ).physical_name
            tcutils.remove_parameters(physical_interface_name)
            self.app.log.info(
                f"Successfully resetted connection {self.app.pargs.connection_name}"
            )
            self.app.close()

    @ex(
        help="deletes all parameters and connection",
    )
    def all(self):
        for connection in dbutils.get_connection_list():
            physical_interface_name = dbutils.get_physical_interface_for_logical_id(
                connection.first_logical_interface_id
            ).physical_name
            tcutils.remove_parameters(physical_interface_name)
            tcutils.remove_connection(connection.connection_name)
        dbutils.reset_all_connections()
        self.app.log.info("Successfullty resetted device")
