# Quickstart
Let's get started with some simple examples.

## Overview
```
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
```

## Configure Management interface(s)
The first step is to configure at least one management interface.
```
$ wemulate config set --help
Usage: main.py config set [OPTIONS]

set the management interface(s)

Options:
-m, --management-interface TEXT
                                [default: ]
--help                          Show this message and exit.
```

```    
$ wemulate config set -m <interface name>
```


```
$ wemulate config set -m ens2 -m eth0
Changing the management interfaces will reset the device.
Do you want to proceed (y / yes)?: y
```

## List all Management interfaces
Lists all management interfaces
```
$ wemulate show mgmt-interfaces
+--------+-------------+-------------------+
| NAME   | IP          | MAC               |
+========+=============+===================+
| ens2   | 10.18.10.10 | 52:54:00:8c:9b:ff |
+--------+-------------+-------------------+
| eth0   |             | 52:54:00:ce:44:b2 |
+--------+-------------+-------------------+    
```

## List all interfaces
Lists all interfaces which are available to configure traffic control.
```
$ wemulate show interfaces
+--------+------------+------+-------------------+
| NAME   | PHYSICAL   | IP   | MAC               |
+========+============+======+===================+
| LAN-A  | ens3       | N/A  | 52:54:00:c5:84:df |
+--------+------------+------+-------------------+
| LAN-B  | ens4       | N/A  | 52:54:00:55:ae:7a |
+--------+------------+------+-------------------+
```

## Add Connection
Adds a new connection on which traffic control can be applied.
```
$ wemulate add connection -n <connection name> -i <interface name 1> <interface name 2>
```
```
$ wemulate add connection -n test -i LAN-A LAN-B
Successfully added a new connection
```

## Delete Connection
Deletes an existing connection and its parameters.
```
$ wemulate delete connection <connection name>
```
```
$ wemulate delete connection test
connection test successfully deleted
```

## List Connections
Lists all available connections and information.
```
$ wemulate show connections
+---------+----------------+----------------+---------------------+
| NAME    | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+=========+================+================+=====================+
| test    | LAN-A          | LAN-B          | <-- delay: 100      |
|         |                |                | --> delay: 250      | 
|         |                |                | <-> jitter: 10      |
|         |                |                | <-- packet_loss: 80 |
+---------+----------------+----------------+---------------------+
| test2   | LAN-C          | LAN-D          |                     |
+---------+-----------------+---------------+---------------------+
```

## List specific Connection
Lists only a specific connection and its related information.
```
$ wemulate show connection <connection name>
```
```
$ wemulate show connection test
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-- delay: 100      |
|        |                |                | <-> jitter: 10      |
|        |                |                | <-- packet_loss: 80 |
+--------+----------------+----------------+---------------------+
```

## Add Parameters to Connection
By adding parameters to a connection, the parameters which are already set on this connection will not be changed!
If the parameter type is already existing, the value and direction will be updated.
If the source and destination are omitted the parameter will be applied birectional.
```
$ wemulate add parameter
Usage: wemulate add parameter [OPTIONS]

  add parameter on a specific connection, previously added parameters will not
  be changed

Options:
  -n, --connection-name TEXT  [required]
  -d, --delay INTEGER
  -j, --jitter INTEGER
  -b, --bandwidth INTEGER
  -l, --packet-loss INTEGER
  -src, --source TEXT
  -dst, --destination TEXT
  --help                      Show this message and exit.
```
```
$ wemulate add parameter -n <connection name> -b <bandwidth value> -j <jitter value> -d <delay value> -l <packet loss value> -src <interface name> -dst <interface name>
```
```
$ wemulate show connections
+--------+----------------+----------------+--------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS   |
+========+================+================+==============+
| test   | LAN-A          | LAN-B          |              |
+--------+----------------+----------------+--------------+

$ wemulate add parameter -n test -l 80 -d 100 -src LAN-B -dst LAN-A
successfully added parameters to connection test

$ wemulate show connections
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-- delay: 100      |
|        |                |                | <-- packet_loss: 80 |
+--------+----------------+----------------+---------------------+

$ wemulate add parameter -n test -d 50
successfully added parameters to connection test

$ wemulate show connections
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-> delay: 50       |
|        |                |                | <-- packet_loss: 80 |
+--------+----------------+----------------+---------------------+

$ wemulate add parameter -n test -j 10 
successfully added parameters to connection test

$ wemulate show connections
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-> delay: 50       |
|        |                |                | --> jitter: 10      |
|        |                |                | <-- packet_loss: 80 |
+--------+----------------+----------------+---------------------+
```
    
## Set Parameters on Connection
When setting parameters on a connection, the parameters which are already set are overwritten by the new parameters!
When no direction is given the parameter is applied bidirectional, which means all other parameters are overwritten.
If a direction is given, only the parameter in this direction are overwritten.
```
$ wemulate set parameter

Usage: wemulate set parameter [OPTIONS]

  set parameter on a specific connection, previously added parameters will be
  overriden

Options:
  -n, --connection-name TEXT  [required]
  -d, --delay INTEGER
  -j, --jitter INTEGER
  -b, --bandwidth INTEGER
  -l, --packet-loss INTEGER
  -src, --source TEXT
  -dst, --destination TEXT
  --help                      Show this message and exit.
```
```
$ wemulate set parameter -n <connection name> -b <bandwidth value> -j <jitter value> -d <delay value> -l <packet loss value> -src <interface name> -dst <interface name>
```
```
$ wemulate show connections
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-- bandwidth: 10   |
|        |                |                | --> packet_loss: 10 |
+--------+----------------+----------------+---------------------+

$ wemulate set parameter -n test -d 20 -src LAN-A -dst LAN-B
successfully added parameters to connection test 

$ wemulate show connection
+--------+----------------+----------------+-------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS        |
+========+================+================+===================+
| test   | LAN-A          | LAN-B          | <-- bandwidth: 10 |
|        |                |                | --> delay: 20     |
+--------+----------------+----------------+-------------------+

$ wemulate set parameter -n test -j 100 -b 100
successfully set parameters to connection test 


$ wemulate show connection
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-> bandwidth: 100  |
|        |                |                | <-> jitter: 100     |
+--------+----------------+----------------+---------------------+


$ wemulate set parameter -n test -d 20
successfully set parameters to connection test

$ wemulate show connections
+--------+----------------+----------------+---------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS    |
+========+================+================+===============+
| test   | LAN-A          | LAN-B          | <-> delay: 20 |
+--------+----------------+----------------+---------------+
```

## Delete parameter on Connection
Delete parameter(s) on a specific connection.
If source and destination information is not given the parameter will removed completely.
```
$ wemulate show connections
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-- delay: 100      |
|        |                |                | <-> jitter: 10      |
|        |                |                | <-- packet_loss: 80 |
+--------+----------------+----------------+---------------------+

$ wemulate delete parameter -n test -j -src LAN-A -dst LAN-B
Successfully deleted parameter on connection test

$ wemulate show connections
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-- delay: 100      |
|        |                |                | <-- jitter: 10      |
|        |                |                | <-- packet_loss: 80 |
+--------+----------------+----------------+---------------------+

$ wemulate delete parameter -n test -j
Successfully deleted parameter on connection test

$ wemulate show connections
+--------+----------------+----------------+---------------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS          |
+========+================+================+=====================+
| test   | LAN-A          | LAN-B          | <-- delay: 100      |
|        |                |                | <-- packet_loss: 80 |
+--------+----------------+----------------+---------------------+

$ wemulate delete parameter -n test -l -src LAN-B -dst LAN-A
Successfully deleted parameter on connection test

$ wemulate show connections
+--------+----------------+----------------+----------------+
| NAME   | 1. INTERFACE   | 2. INTERFACE   | PARAMETERS     |
+========+================+================+================+
| test   | LAN-A          | LAN-B          | <-- delay: 100 |
+--------+----------------+----------------+----------------+
```

## Reset Connection
All parameters on a specific connection will be resettet.
```
$ wemulate reset connection <connection name>
```
```
$ wemulate reset connection test
Successfully resetted connection test 
```

## Reset Device
All parameters and connections will be resettet.
```
$ wemulate reset device
Successfully resetted device
```
    