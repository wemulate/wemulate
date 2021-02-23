from cement import Controller, ex

class LoadController(Controller):
    class Meta:
        label = 'load'

        stacked_on = 'base'
        stacked_type = 'nested'

        help='example sub command1'
        arguments=[
            ( [ '-f', '--file-location' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'file_location' } )
        ]