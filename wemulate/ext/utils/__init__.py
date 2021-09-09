from wemulate.ext.utils.retrieve import get_physical_interface_names
from wemulate.ext.utils.reset import reset_device, reset_connection
from wemulate.ext.utils.add import add_connection, add_parameter
from wemulate.ext.utils.set import set_parameter
from wemulate.ext.utils.common import (
    create_or_update_parameters_in_db,
    set_parameters_with_tc,
    delete_parameters_in_db,
)
from wemulate.ext.utils.delete import delete_connection, delete_parameter