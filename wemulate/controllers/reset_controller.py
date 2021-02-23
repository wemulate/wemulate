from cement import Controller, ex

class ResetController(Controller):
    class Meta:
        label = 'reset'

        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(
        help='example sub command1',
        arguments=[
            ( [ '-n', '--connection-name' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'connection_name' } )
        ],
    )
    def connection(self):
        if self.app.pargs.connection_name is not None:
            self.app.log.info(self.app.pargs.connection_name)

    @ex(
        help='example sub command1',
    )
    def all(self):
        self.app.log.error('test')