from cement import Controller, ex

class ShowController(Controller):
    class Meta:
        label = 'show'
        help = 'show specific informations'
        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(
        help='Show specific Connection Information',
        arguments=[
            ( ['connection_name'],
              {'help': 'Name of the Connection'} )
        ],
    )
    def connection(self):
        self.app.log.info(self.app.pargs.connection_name)
        
    @ex(
        help='Show Overview about all Connections',
    )
    def connections(self):
        self.app.log.info('All connections will be listed here')

    @ex(
        help='Show specific Interface Information',
        arguments=[
            ( ['interface_name'],
              {'help': 'Name of the Interface'} )
        ],
    )
    def interface(self):
        self.app.log.info(self.app.pargs.interface_name)
        
    @ex(
        help='Show Overview about all Interfaces',
    )
    def interfaces(self):
        self.app.log.info('All Interfaces will be listed here')

    @ex(
        help='Show Overview about all Management Interfaces',
    )
    def mgmt_interfaces(self):
        self.app.log.info('All Management Interfaces will be listed here')