from cement import Controller, ex


class SaveController(Controller):

    #### NOT IMPLEMENTED YET ###
    class Meta:
        label = "save"
        help = "save the current configuration"
        stacked_on = "base"
        stacked_type = "nested"

        arguments = [
            (
                ["-f", "--file-location"],
                {
                    "help": "notorious foo option",
                    "action": "store",
                    "dest": "file_location",
                },
            )
        ]
