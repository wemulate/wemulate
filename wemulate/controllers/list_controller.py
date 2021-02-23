from cement import Controller, ex

class ListController(Controller):
    class Meta:
        label = 'list'
        help = 'list specific informations'
        stacked_on = 'base'
        stacked_type = 'nested'
        
    @ex(
        help='List all Connections',
    )
    def connections(self):
        self.app.log.info('All connections will be listed here')
        
    @ex(
        help='List all Interfaces',
    )
    def interfaces(self):
        self.app.log.info('All Interfaces will be listed here')

    @ex(
        help='List all Management Interfaces',
    )
    def mgmt_interfaces(self):
        self.app.log.info('All Management Interfaces will be listed here')