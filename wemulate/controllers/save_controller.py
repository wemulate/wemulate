from cement import Controller, ex

class SaveController(Controller):
    class Meta:
        label = 'save'

        stacked_on = 'base'
        stacked_type = 'nested'

        help='example sub command1'
        arguments=[
            ( [ '-f', '--file-location' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'file_location' } )
        ]