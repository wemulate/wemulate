.. _api:

API Specification
#####################

This site contains information about the different API routes. 
The API package has to be installed on the system to use the appropriate routes.

GET ``/api/v1/device/``
***********************

Get general device information.

Response
======================

.. code-block:: json 

    {
        "mgmt_interfaces" : [
            {
                "ip": "192.168.1.1",
                "physical_name": "ens0"
            },
            {
                "ip": "10.10.10.10",
                "physical_name": "ens1"
            }
        ],
        "interfaces": [
            {
                "interface_id": 1,
                "logical_name": "LAN A",
                "physical_name": "eth1",
            },
            {
                "interface_id": 2,
                "logical_name": "LAN B",
                "physical_name": "eth2",
            },
            {
                "interface_id": 3,
                "logical_name": "LAN C",
                "physical_name": "eth3",
            },
            {
                "interface_id": 4,
                "logical_name": "LAN D",
                "physical_name": "eth4",
            }
        ],
    }


GET ``/api/v1/connections/``
******************************

Get all connection information.

Response
======================

.. code-block:: json

    {
        "connections": [
            {
                "connection_name": "Connection1",
                "connection_id": 1,
                "first_logical_interface": 1,
                "second_logical_interface": 2,
                "delay": 0,
                "packet_loss": 5,
                "bandwidth": 100,
                "jitter": 5
            },
            {
                "connection": "Connection2",
                "connection_id": 2,
                "first_logical_interface": "LAN C",
                "second_logical_interface": "LAN D",
                "delay": 0,
                "packet_loss": 5,
                "bandwidth": 100,
                "jitter": 5
            }
        ]    
    }

POST ``/api/v1/connections/``
*******************************

Create a single connection.

Request
======================

.. code-block:: json

    {
        "connection_name": "new_name",
        "first_logical_interface": 2,
        "second_logical_interface": 3,
    }

Response
======================

.. code-block:: json

    {
        "connection_name": "new_name",
        "connection_id": 2,
        "first_logical_interface": 2,
        "second_logical_interface": 3,
    }

GET ``/api/v2/connections/<connection_id>/``
**********************************************

Get specific connection information.

Response
======================

.. code-block:: json

    {
        "connection_name": "Connection2",
        "connection_id": 2,
        "first_logical_interface": 2,
        "second_logical_interface": 3,
        "delay": 1,
        "packet_loss": 6,
        "bandwidth": 101,
        "jitter": 6
    }

PUT ``/api/v2/connections/<connection_id>/``
**********************************************

Update specific connection information.

Request
======================

.. code-block:: json

    {
        "connection_name": "new-name",
        "connection_id": 2,
        "first_logical_interface": 2,
        "second_logical_interface": 3,
        "delay": 1,
        "packet_loss": 6,
        "bandwidth": 101,
        "jitter": 6
    }


Response
======================

.. code-block:: json

    {
        "connection_name": "new-name",
        "connection_id": 2,
        "first_logical_interface": 2,
        "second_logical_interface": 3,
        "delay": 1,
        "packet_loss": 6,
        "bandwidth": 101,
        "jitter": 6
    }