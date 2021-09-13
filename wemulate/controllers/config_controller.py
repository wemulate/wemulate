from cement import Controller, ex


class ConfigController(Controller):
    class Meta:
        label = "config"
        help = "configure the application settings"
        stacked_on = "base"
        stacked_type = "nested"

    #### NOT IMPLEMENTED YET ###

    @ex(
        help="example sub command1",
        arguments=[
            (
                ["-i", "--interfaces"],
                {
                    "help": "notorious foo option",
                    "action": "store",
                    "dest": "interfaces",
                },
            )
        ],
    )
    def mgmt_interfaces(self):
        if self.app.pargs.interfaces is not None:
            self.app.log.info(self.app.pargs.interfaces)
