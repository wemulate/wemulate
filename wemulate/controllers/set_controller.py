from cement import Controller, ex

class SetController(Controller):
    class Meta:
        label = 'set'

        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(
        help='example sub command1',
        arguments=[
            ( [ '-n', '--connection-name' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'connection_name' } ),
            ( [ '-b', '--bandwidth' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'bandwidth' } ),
            ( [ '-j', '--jitter' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'jitter' } ),
            ( [ '-d', '--delay' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'delay' } ),
            ( [ '-l', '--packet-loss' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'packet-loss' } )
        ],
    )
    def parameter(self):
        if self.app.pargs.connection_name is not None:
            self.app.log.error('test')