from cement import Controller, ex
import netifaces

from wemulate.utils.helper import get_interfaces, get_mgmt_interfaces

class ShowController(Controller):
    class Meta:
        label = 'show'
        help = 'show specific informations'
        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(
        help='show specific connection information',
        arguments=[
            ( ['connection_name'],
              {'help': 'name of the connection'} )
        ],
    )
    def connection(self):
        self.app.log.info(self.app.pargs.connection_name)
        
    @ex(
        help='show overview about all connections',
    )
    def connections(self):
        self.app.log.info('all connections will be listed here')

    @ex(
        help='show specific interface information',
        arguments=[
            ( ['interface_name'],
              {'help': 'name of the interface'} )
        ],
    )
    def interface(self):
        self.app.log.info(self.app.pargs.interface_name)
        
    @ex(
        help='show overview about all interfaces',
    )
    def interfaces(self):
        headers = ['NAME', 'IP', 'MAC']
        data = []

        for int in get_interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(int):
                ip = netifaces.ifaddresses(int)[netifaces.AF_INET][0]['addr']
            else:
                ip = 'N/A'
                
            data.append([int, ip, netifaces.ifaddresses(int)[netifaces.AF_LINK][0]['addr']])

        self.app.render(data, headers=headers)


    @ex(
        help='show overview about all management interfaces',
    )
    def mgmt_interfaces(self):
        headers = ['NAME', 'IP', 'MAC']
        data = []
        for int in get_mgmt_interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(int):
                ip = netifaces.ifaddresses(int)[netifaces.AF_INET][0]['addr']
            else:
                ip = 'N/A'
                
            data.append([int, ip, netifaces.ifaddresses(int)[netifaces.AF_LINK][0]['addr']])


        self.app.render(data, headers=headers)