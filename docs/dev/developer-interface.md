# Developer Interface
This part of the documentation covers all the interfaces of WEmulate.

## Database and TC Interface
::: wemulate.ext.utils.add_connection
::: wemulate.ext.utils.add_parameter
::: wemulate.ext.utils.set_parameter
::: wemulate.ext.utils.create_or_update_parameters_in_db
    options:
        docstring_style: 
::: wemulate.ext.utils.set_parameters_with_tc
    options:
        docstring_style: 
::: wemulate.ext.utils.delete_parameters_in_db
::: wemulate.ext.utils.get_current_applied_parameters
    options:
        docstring_style: 
::: wemulate.ext.utils.delete_connection
::: wemulate.ext.utils.delete_parameter
::: wemulate.ext.utils.reset_connection
::: wemulate.ext.utils.reset_device
::: wemulate.ext.utils.get_physical_interface_names
::: wemulate.ext.utils.get_logical_interface_by_name
::: wemulate.ext.utils.connection_exists_in_db
::: wemulate.ext.utils.get_connection_by_name
::: wemulate.ext.utils.get_connection_by_id
::: wemulate.ext.utils.get_logical_interface_by_physical_name
::: wemulate.ext.utils.get_logical_interface_by_id
::: wemulate.ext.utils.get_connection_list
::: wemulate.ext.utils.reset_connection
::: wemulate.ext.utils.reset_device


## Setting and Configuration Interface
::: wemulate.ext.settings.get_interface_ip
::: wemulate.ext.settings.get_interface_mac_address
::: wemulate.ext.settings.get_mgmt_interfaces
::: wemulate.ext.settings.get_all_interfaces_on_device
::: wemulate.ext.settings.add_mgmt_interface
::: wemulate.ext.settings.get_non_mgmt_interfaces
::: wemulate.ext.settings.check_if_mgmt_interface_set
::: wemulate.ext.settings.get_db_location
::: wemulate.ext.settings.check_if_interface_present_on_device


## Exceptions
::: wemulate.core.exc.WEmulateError
::: wemulate.core.exc.WEmulateValidationError
::: wemulate.core.exc.WEmulateExecutionError
::: wemulate.core.exc.WEmulateConfigNotFoundError
::: wemulate.core.exc.WEmulateFileError
::: wemulate.core.exc.WEmulateDatabaseError
::: wemulate.core.exc.WemulateMgmtInterfaceError
