# Installation
This part of the documentation covers the installation of WEmulate.


## Requirements
In order to use WEmulate to influence traffic at least the following requirements should be fulfilled:

* At least two network interfaces for `LAN-A` and `LAN-B`
* A third management interface if you would like to use the api and frontend module
* Ubuntu installed
* Root permissions


## Install with bash
To install only the WEmulate cli with bash, simply run this command in your terminal of choice:
```
$ bash -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)"
```

There are different arguments available in order to enhance the installation experience:

* `-h` Prints the help message
* `-f` Skip the confirmation prompt during installation
* `-i <int1,int2>` List of interfaces which should be used as management interfaces
* `-a` Installs the api module
* `-v` Installs the frontend module

You can for example install the cli, api and frontend module together with one management interface with the following command:
```
$ curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh | bash -s -- -a -v -i ens2 -f
```

## Install from source
You can also install WEmulate from source, please follow the instructions below:

* Install poetry (see [here](https://python-poetry.org/docs/#installation) for more information)

* Install all dependencies:
```
$ sudo apt install --yes python3 python3-pip 
```
* Clone the repository
```
$ git clone https://github.com/wemulate/wemulate
```
* Install WEmulate
```
$ cd wemulate
$ poetry install
```
* Configure the management interfaces
```
$ wemulate config set -m ens2
```