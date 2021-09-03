from cement import Controller, ex


class LoadController(Controller):

    #### NOT IMPLEMENTED YET ###
    class Meta:
        label = "load"
        help = "load a saved configuration"
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
