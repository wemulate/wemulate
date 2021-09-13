import wemulate.ext.utils as utils
import wemulate.controllers.common as common
from cement import Controller, ex


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
            utils.set_parameter(
                self.app.pargs.connection_name, common.generate_pargs(self)
            )
            self.app.log.info(
                f"Successfully set parameters on connection {self.app.pargs.connection_name}"
            )
            self.app.close()
