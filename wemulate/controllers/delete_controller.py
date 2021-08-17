import wemulate.utils.tcconfig as tcutils
import wemulate.core.database.utils as dbutils
import wemulate.controllers.common as common
from typing import Dict
from wemulate.core.database.models import (
    BANDWIDTH,
    DELAY,
    JITTER,
    PACKET_LOSS,
    ConnectionModel,
)
from cement import Controller, ex


class DeleteController(Controller):
    class Meta:
        label = "delete"
        help = "delete connection or parameter"
        stacked_on = "base"
        stacked_type = "nested"

    def _delete_bandwidth(
        self, parameters: Dict[str, int], connection: ConnectionModel
    ) -> None:
        if self.app.pargs.bandwidth:
            parameters.pop(BANDWIDTH)
            dbutils.delete_parameter_on_connection_id(
                connection.connection_id,
                BANDWIDTH,
            )

    def _delete_jitter(
        self, parameters: Dict[str, int], connection: ConnectionModel
    ) -> None:
        if self.app.pargs.jitter:
            parameters.pop(JITTER)
            dbutils.delete_parameter_on_connection_id(connection.connection_id, JITTER)

    def _delete_delay(
        self, parameters: Dict[str, int], connection: ConnectionModel
    ) -> None:
        if self.app.pargs.delay:
            parameters.pop(DELAY)
            dbutils.delete_parameter_on_connection_id(connection.connection_id, DELAY)

    def _delete_packet_loss(
        self, parameters: Dict[str, int], connection: ConnectionModel
    ) -> None:
        if self.app.pargs.packet_loss:
            parameters.pop(PACKET_LOSS)
            dbutils.delete_parameter_on_connection_id(
                connection.connection_id,
                PACKET_LOSS,
            )

    def _delete_parameters(
        self, parameters: Dict[str, int], connection: ConnectionModel
    ) -> None:
        self._delete_bandwidth(parameters, connection)
        self._delete_jitter(parameters, connection)
        self._delete_delay(parameters, connection)
        self._delete_packet_loss(parameters, connection)

    @ex(
        help="delete a specific connection",
        arguments=[
            common.CONNECTION_NAME_ARGUMENT,
        ],
    )
    def connection(self):
        if not common.connection_name_is_set(
            self
        ) or not common.connection_exists_in_db(self.app.pargs.connection_name):
            self.app.close()
        else:
            tcutils.remove_connection(self.app.pargs.connection_name)
            dbutils.delete_connection_by_name(self.app.pargs.connection_name)
            self.app.log.info(
                f"connection {self.app.pargs.connection_name} successfully deleted"
            )

    @ex(
        help="delete a specific parameter on a connection",
        arguments=[
            common.CONNECTION_NAME_ARGUMENT,
            common.BANDWIDTH_ARGUMENT,
            common.JITTER_ARGUMENT,
            common.PACKET_LOSS_ARGUMENT,
        ],
    )
    def parameter(self):
        if not common.connection_exists_in_db(
            self
        ) or not common.validate_parameter_arguments(self):
            self.app.close()
        else:
            connection: ConnectionModel = dbutils.get_connection(
                self.app.pargs.connection_name
            )
            parameters: Dict[
                str, int
            ] = dbutils.get_all_parameter_values_for_connection_id(
                connection.connection_id
            )

            if not parameters:
                self.app.log.info("There are no parameters set on this connection")
                self.app.close()
            else:
                self._delete_parameters(parameters, connection)
                physical_interface_name = dbutils.get_physical_interface_for_logical_id(
                    connection.first_logical_interface_id
                ).physical_name
                tcutils.remove_parameters(physical_interface_name)
                tcutils.set_parameters(
                    physical_interface_name,
                    parameters,
                )
                self.app.log.info(
                    f"Successfully deleted parameter on connection {self.app.pargs.connection_name}"
                )
