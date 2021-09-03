from typing import Dict
import wemulate.core.database.utils as dbutils
import wemulate.utils.tcconfig as tcutils
import wemulate.controllers.common as common
from cement import Controller, ex
from wemulate.core.database.models import (
    BANDWIDTH,
    ConnectionModel,
    JITTER,
    DELAY,
    PACKET_LOSS,
)


class SetController(Controller):
    class Meta:
        label = "set"
        help = "set specific parameter on connections"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="set parameters on a specific connection, all parameters will be overridden",
        arguments=[
            common.CONNECTION_NAME_ARGUMENT,
            common.PARAMETER_ARGUMENT_MAP["DELAY_STORE"],
            common.PARAMETER_ARGUMENT_MAP["JITTER_STORE"],
            common.PARAMETER_ARGUMENT_MAP["BANDWIDTH_STORE"],
            common.PARAMETER_ARGUMENT_MAP["PACKET_LOSS_STORE"],
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
            connection: ConnectionModel = dbutils.get_connection(
                self.app.pargs.connection_name
            )
            dbutils.delete_all_parameter_on_connection(connection.connection_id)
            parameters: Dict[str, int] = {}
            common.create_or_update_parameters_in_db(self, connection, parameters)
            tcutils.set_parameters(
                self.app.pargs.connection_name,
                dbutils.get_physical_interface_for_logical_id(
                    connection.first_logical_interface_id
                ).physical_name,
                parameters,
            )
            self.app.log.info(
                f"Successfully set parameters on connection {self.app.pargs.connection_name}"
            )
            self.app.close()
