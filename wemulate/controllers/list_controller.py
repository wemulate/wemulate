from cement import Controller, ex

from wemulate.utils.helper import get_interfaces, get_mgmt_interfaces

class ListController(Controller):
    class Meta:
        label = 'list'
        help = 'list specific informations'
        stacked_on = 'base'
        stacked_type = 'nested'
        
    @ex(
        help='list all connections',
    )
    def connections(self):
        self.app.log.info('all connections will be listed here')
        
    @ex(
        help='list all interfaces',
    )
    def interfaces(self):
        data = {'interfaces': get_interfaces()}
        self.app.render(data, 'list_interfaces.jinja2', handler='jinja2')

    @ex(
        help='list all management interfaces',
    )
    def mgmt_interfaces(self):
        data = {'interfaces': get_mgmt_interfaces()}
        self.app.render(data, 'list_interfaces.jinja2', handler='jinja2')