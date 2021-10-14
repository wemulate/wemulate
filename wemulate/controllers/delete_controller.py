import wemulate.ext.utils as utils
import wemulate.controllers.common as common
from typing import Dict
from wemulate.core.database.models import ConnectionModel
from cement import Controller, ex


class DeleteController(Controller):
    class Meta:
        label = "delete"
        help = "delete connection or parameter"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="delete a specific connection",
        arguments=[
            common.CONNECTION_NAME_ARGUMENT,
        ],
    )
    def connection(self):
        if not common.connection_name_is_set(
            self
        ) or not common.connection_exists_in_db(self):
            self.app.close()
        else:
            utils.delete_connection(self.app.pargs.connection_name)
            self.app.log.info(
                f"connection {self.app.pargs.connection_name} successfully deleted"
            )

    @ex(
        help="delete a specific parameter on a connection",
        arguments=[
            common.CONNECTION_NAME_ARGUMENT,
            common.PARAMETER_ARGUMENT_MAP["DELAY_STORE_TRUE"],
            common.PARAMETER_ARGUMENT_MAP["JITTER_STORE_TRUE"],
            common.PARAMETER_ARGUMENT_MAP["BANDWIDTH_STORE_TRUE"],
            common.PARAMETER_ARGUMENT_MAP["PACKET_LOSS_STORE_TRUE"],
        ],
    )
    def parameter(self):
        if (
            not common.connection_name_is_set(self)
            or not common.connection_exists_in_db(self)
            or not common.validate_parameter_arguments(self)
        ):
            self.app.close()
        else:
            connection: ConnectionModel = utils.get_connection_by_name(
                self.app.pargs.connection_name
            )
            parameters: Dict[str, int] = {
                parameter.parameter_name: parameter.value
                for parameter in connection.parameters
            }
            if not parameters:
                self.app.log.info("There are no parameters set on this connection")
                self.app.close()
            else:
                utils.delete_parameter(
                    self.app.pargs.connection_name, common.generate_pargs(self)
                )
                self.app.log.info(
                    f"Successfully deleted parameter on connection {self.app.pargs.connection_name}"
                )
