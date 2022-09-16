.. _developer-interface:

Developer Interface
#####################

.. module:: wemulate

This part of the documentation covers all the interfaces of WEmulate.

Database and TC Interface
*************************
.. autofunction:: wemulate.ext.utils.add_connection
.. autofunction:: wemulate.ext.utils.add_parameter
.. autofunction:: wemulate.ext.utils.set_parameter
.. autofunction:: wemulate.ext.utils.create_or_update_parameters_in_db
.. autofunction:: wemulate.ext.utils.set_parameters_with_tc
.. autofunction:: wemulate.ext.utils.delete_parameters_in_db
.. autofunction:: wemulate.ext.utils.get_current_applied_parameters
.. autofunction:: wemulate.ext.utils.delete_connection
.. autofunction:: wemulate.ext.utils.delete_parameter
.. autofunction:: wemulate.ext.utils.reset_connection
.. autofunction:: wemulate.ext.utils.reset_device
.. autofunction:: wemulate.ext.utils.get_physical_interface_names
.. autofunction:: wemulate.ext.utils.get_logical_interface_by_name
.. autofunction:: wemulate.ext.utils.connection_exists_in_db
.. autofunction:: wemulate.ext.utils.get_connection_by_name
.. autofunction:: wemulate.ext.utils.get_connection_by_id
.. autofunction:: wemulate.ext.utils.get_logical_interface_by_physical_name
.. autofunction:: wemulate.ext.utils.get_logical_interface_by_id
.. autofunction:: wemulate.ext.utils.get_connection_list


Setting and Configuration Interface
***********************************
.. autofunction:: wemulate.ext.settings.get_interface_ip
.. autofunction:: wemulate.ext.settings.get_interface_mac_address
.. autofunction:: wemulate.ext.settings.get_mgmt_interfaces
.. autofunction:: wemulate.ext.settings.get_all_interfaces_on_device
.. autofunction:: wemulate.ext.settings.add_mgmt_interface
.. autofunction:: wemulate.ext.settings.get_non_mgmt_interfaces
.. autofunction:: wemulate.ext.settings.check_if_mgmt_interface_set
.. autofunction:: wemulate.ext.settings.get_db_location


Exceptions
*************
.. autoexception:: wemulate.core.exc.WEmulateError
.. autoexception:: wemulate.core.exc.WEmulateValidationError
.. autoexception:: wemulate.core.exc.WEmulateExecutionError
.. autoexception:: wemulate.core.exc.WEmulateConfigNotFoundError
.. autoexception:: wemulate.core.exc.WEmulateFileError
.. autoexception:: wemulate.core.exc.WEmulateDatabaseError
.. autoexception:: wemulate.core.exc.WemulateMgmtInterfaceError
