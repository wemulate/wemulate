from cement import Controller, ex

import os

BRIDGE_CONFIG_PATH = "/etc/network/interfaces.d"
INTERFACE_CONFIG_PATH = "/etc/network/interfaces"


class AddController(Controller):
    class Meta:
        label = "add"
        help = "add a new connection or parameter"
        stacked_on = "base"
        stacked_type = "nested"

    @ex(
        help="example sub command1",
        # arguments=[
        #     ( [ '-n', '--connection-name' ],
        #       { 'help' : 'notorious foo option',
        #         'action'  : 'store',
        #         'dest' : 'connection_name' } ),
        #     ( [ '-i', '--interfaces' ],
        #       { 'help' : 'notorious foo option',
        #         'action'  : 'store',
        #         'dest' : 'interfaces_list' } ),
        #     ( [ 'extra_arguments' ],
        #       { 'action'  : 'store',
        #         'nargs' : '*' } )
        # ],
        arguments=[
            (
                ["-n", "--connection-name"],
                {
                    "help": "notorious foo option",
                    "action": "store",
                    "dest": "connection_name",
                },
            ),
            (
                ["-i", "--interfaces"],
                {"help": "notorious foo option", "action": "store", "nargs": "*"},
            ),
        ],
    )
    def connection(self):
        # with open(INTERFACE_CONFIG_PATH, 'r+') as interfaces_config_file:
        #     if BRIDGE_CONFIG_PATH not in interfaces_config_file.read():
        #         interfaces_config_file.write(f'source {BRIDGE_CONFIG_PATH}/*\n')

        # connection_template = f"# Bridge Setup {self.app.pargs.connection_name}\nauto {self.app.pargs.connection_name}\niface {self.app.pargs.connection_name} inet manual\n    bridge_ports {self.app.pargs.interfaces_list[0]} {self.app.pargs.interfaces_list[1]}\n    bridge_stp off\n"

        # if not os.path.exists('BRIDGE_CONFIG_PATH'):
        #     os.makedirs('BRIDGE_CONFIG_PATH')

        # with open(f"{BRIDGE_CONFIG_PATH}/{self.app.pargs.connection_name}", "w") as connection_file:
        #     connection_file.write(connection_template)
        self.app.log.error(self.app.pargs.interfaces_list)
        self.app.log.error(self.app.pargs.extra_arguments[0])

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
            ),
            (
                ["-b", "--bandwidth"],
                {
                    "help": "notorious foo option",
                    "action": "store",
                    "dest": "bandwidth",
                },
            ),
            (
                ["-j", "--jitter"],
                {"help": "notorious foo option", "action": "store", "dest": "jitter"},
            ),
            (
                ["-d", "--delay"],
                {"help": "notorious foo option", "action": "store", "dest": "delay"},
            ),
            (
                ["-l", "--packet-loss"],
                {
                    "help": "notorious foo option",
                    "action": "store",
                    "dest": "packet-loss",
                },
            ),
        ],
    )
    def parameter(self):
        if self.app.pargs.connection_name is not None:
            self.app.log.error("test")
