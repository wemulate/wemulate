from cement import Controller, ex

class DeleteController(Controller):
    class Meta:
        label = 'delete'

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
        if self.app.pargs.connection_name is None:
            self.app.log.error('test')

    @ex(
        help='example sub command1',
        arguments=[
            ( [ '-n', '--connection-name' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'connection_name' } ),
            ( [ '-b', '--bandwidth' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store_true'} ),
            ( [ '-j', '--jitter' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store_true'} ),
            ( [ '-d', '--delay' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store_true'} ),
            ( [ '-l', '--packet-loss' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store_true'} )
        ],
    )
    def parameter(self):
        if self.app.pargs.connection_name is not None:
            self.app.log.error('test')