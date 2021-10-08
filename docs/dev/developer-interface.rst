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
.. autofunction:: wemulate.ext.settings.get_config
.. autofunction:: wemulate.ext.settings.get_config_path
.. autofunction:: wemulate.ext.settings.get_db_location
.. autofunction:: wemulate.ext.settings.get_interface_mac_address
.. autofunction:: wemulate.ext.settings.get_interfaces
.. autofunction:: wemulate.ext.settings.get_mgmt_interfaces


Exceptions
*************
.. autoexception:: wemulate.core.exc.WEmulateError
.. autoexception:: wemulate.core.exc.WEmulateValidationError
.. autoexception:: wemulate.core.exc.WEmulateExecutionError
