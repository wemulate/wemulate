.. _quickstart:

Quickstart
###########

.. module:: requests.models

Let's get started with some simple examples.

Overview
*********

.. code-block:: console

    $ wemulate
    Usage: main.py [OPTIONS] COMMAND [ARGS]...

    A modern WAN emulator

    Options:
    -v, --version                   Show program's version number and exit
    --install-completion [bash|zsh|fish|powershell|pwsh]
                                    Install completion for the specified shell.
    --show-completion [bash|zsh|fish|powershell|pwsh]
                                    Show completion for the specified shell, to
                                    copy it or customize the installation.

    --help                          Show this message and exit.

    Commands:
    add     add a new connection or parameter
    config  configure the application settings
    delete  delete a connection or parameter
    reset   reset connection or the whole application settings
    set     set parameters on a connection
    show    show specific information

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

    $ wemulate add connection -n <connection name> -i <interface one> <interface two>

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
    Usage: main.py add parameter [OPTIONS]

    add parameter on a specific connection, previously added parameters will
    not be changed

    Options:
    -n, --connection-name TEXT  [required]
    -d, --delay INTEGER
    -j, --jitter INTEGER
    -b, --bandwidth INTEGER
    -l, --packet-loss INTEGER
    --help                      Show this message and exit.

.. code-block:: console

    $ wemulate add parameter -n <connection name> -b <bandwidth value> -j <jitter value> -d <delay value> -l <packet loss value>

Set Parameters on Connection
*****************************
When setting parameters on a connection, the parameters which are already set are overwritten by the new parameters!

.. code-block:: console

    $ wemulate set parameter -h
    Usage: main.py set parameter [OPTIONS]

    set parameter on a specific connection, previously added parameters will
    be overriden

    Options:
    -n, --connection-name TEXT  [required]
    -d, --delay INTEGER
    -j, --jitter INTEGER
    -b, --bandwidth INTEGER
    -l, --packet-loss INTEGER
    --help                      Show this message and exit.

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

Configure Management interfaces
***********************************

.. code-block:: console

    $ wemulate config set --help
    Usage: main.py config set [OPTIONS]

    set the management interface(s)

    Options:
    -m, --management-interface TEXT
                                    [default: ]
    --help                          Show this message and exit.

.. code-block:: console
    
    $ wemulate config set -m <interface name>