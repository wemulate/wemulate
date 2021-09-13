.. _quickstart:

Quickstart
###########

.. module:: requests.models

Let's get started with some simple examples.

Overview
*********

.. code-block:: console

    $ wemulate
    usage: wemulate [-h] [-d] [-q] [-v] {load,save,config,reset,delete,set,list,add,show} ...

    A modern WAN Emulator

    optional arguments:
    -h, --help            show this help message and exit
    -d, --debug           full application debug mode
    -q, --quiet           suppress all console output
    -v, --version         show program's version number and exit

    sub-commands:
    {load,save,config,reset,delete,set,list,add,show}
        load                load a saved configuration
        save                save the current configuration
        config              configuration of the application
        reset               reset connection or program
        delete              delete parameter or connection
        set                 set specific parameter on connections
        list                list specific informations
        add                 add a new connection or parameter
        show                show specific informations


List all Management interfaces
**********************************************
Lists all management interfaces which are defined in the configuration file under ``/etc/wemulate/wemulate.yml``

.. code-block:: console

    $ wemulate show mgmt-interfaces
    +--------+------------+--------------------+
    | NAME   | IP         | MAC                |
    +========+============+====================+
    | ens2   | 192.168.0.1 | 53:54:00:b8:f1:c2 |
    +--------+------------+--------------------+

List all interfaces
***********************
Lists all interfaces which are available to configure traffic control.

.. code-block:: console

    $ wemulate show interfaces
    +--------+------------+------+-------------------+
    | NAME   | PHYSICAL   | IP   | MAC               |
    +========+============+======+===================+
    | LAN-A  | ens3       | N/A  | 52:54:00:c5:84:df |
    +--------+------------+------+-------------------+
    | LAN-B  | ens4       | N/A  | 52:54:00:55:ae:7a |
    +--------+------------+------+-------------------+

Add Connection
***********************
Adds a new connection on which traffic control can be applied.

.. code-block:: console

    $ wemulate add connection -n <connection name> -i <interface one>,<interface two>

Delete Connection
***********************
Deletes an existing connection and its parameters.

.. code-block:: console

    $ wemulate delete connection <connection name>

List Connections
***********************
Lists all available connections and informations.

.. code-block:: console

    $ wemulate show connections
    +---------+-----------------+----------------+----------------+----------------+
    | NAME    | BIDIRECTIONAL   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS     |
    +=========+=================+================+================+================+
    | test1   | True            | LAN-A          | LAN-B          | bandwidth: 100 |
    +---------+-----------------+----------------+----------------+----------------+
    | test2   | True            | LAN-C          | LAN-D          |                |
    +---------+-----------------+----------------+----------------+----------------+

List specific Connection
**************************
Lists only a specific connection and its related information.

.. code-block:: console

    $ wemulate show connection test1
    +---------+-----------------+----------------+----------------+----------------+
    | NAME    | BIDIRECTIONAL   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS     |
    +=========+=================+================+================+================+
    | test1   | True            | LAN-A          | LAN-B          | bandwidth: 100 |
    +---------+-----------------+----------------+----------------+----------------+

Add Parameters to Connection
*******************************
By adding parameters to a connection, the parameters which are already set on this connection will not be changed!

.. code-block:: console

    $ wemulate add parameter -h
    usage: wemulate add parameter [-h] [-n CONNECTION_NAME] [-b BANDWIDTH] [-j JITTER] [-d DELAY] [-l PACKET_LOSS]

    optional arguments:
    -h, --help            show this help message and exit
    -n CONNECTION_NAME, --connection-name CONNECTION_NAME
                            name of the connection on which the parameters should be applied
    -b BANDWIDTH, --bandwidth BANDWIDTH
                            bandwidth parameter in mbps
    -j JITTER, --jitter JITTER
                            jitter parameter
    -d DELAY, --delay DELAY
                            delay parameter in ms
    -l PACKET_LOSS, --packet-loss PACKET_LOSS
                            packet loss parameter in percentage

.. code-block:: console

    $ wemulate add parameter -n <connection name> -b <bandwidth value> -j <jitter value> -d <delay value> -l <packet loss value>

Set Parameters on Connection
*****************************
When setting parameters on a connection, the parameters which are already set are overwritten by the new parameters!

.. code-block:: console

    $ wemulate set parameter -h
    usage: wemulate set parameter [-h] [-n CONNECTION_NAME] [-b BANDWIDTH] [-j JITTER] [-d DELAY] [-l PACKET_LOSS]

    optional arguments:
    -h, --help            show this help message and exit
    -n CONNECTION_NAME, --connection-name CONNECTION_NAME
                            name of the connection on which the parameters should be applied
    -b BANDWIDTH, --bandwidth BANDWIDTH
                            bandwidth parameter in mbps
    -j JITTER, --jitter JITTER
                            jitter parameter
    -d DELAY, --delay DELAY
                            delay parameter in ms
    -l PACKET_LOSS, --packet-loss PACKET_LOSS
                            packet loss parameter in percentage

.. code-block:: console

    $ wemulate set parameter -n <connection name> -b <bandwidth value> -j <jitter value> -d <delay value> -l <packet loss value>


Reset Connection
*****************************
All parameters on a specific connection will be resettet.

.. code-block:: console

    $ wemulate reset connection <connection name>

Reset Device
*****************************
All parameters and connections will be resettet.

.. code-block:: console

    $ wemulate reset device

