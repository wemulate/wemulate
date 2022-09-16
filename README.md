**A modern WAN Emulator developed by the Institute for Networked Solutions**
# WEmulate

Have a look at the [documentation](https://wemulate.github.io/wemulate) for detailed information.

## Installation

### Prerequisites
* Virtual machine or physical device with at least two interfaces
* Root permissions 

### Getting Started
Install wemulate cli application  
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)"
```
You have different options available over the install script:
```
Syntax: install.sh [-h|f|i|v|a]
options:
-h               Print this Help.
-f               Force install.
-i <int1,int2>   Management interfaces to configure.
-v               Install frontend module.
-a               Install api module.
```
You can for example install the cli, api and frontend module together with two management interfaces with the following command:
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)" -a -v -i ens2,ens3 -f
```

## Usage 
![WEmulate CLI Commands](/docs/img/animation-wemulate-cli.gif)

```bash
# Add a new connection
$ wemulate add connection -n connectionname -i LAN-A LAN-B

# Delete a connection
$ wemulate delete connection -n connectionname

# Add parameters bidirectional
$ wemulate add parameter -n connectionname -j 20 -d 40

# Add parameters in specific direction
$ wemulate add parameter -n connectionname -j 20 -d 40 -src LAN-A -dst LAN-B

```

## Development
Configure poetry to create the environment inside the project path, in order that VSCode can recognize the virtual environment.
```
$ poetry config virtualenvs.in-project true
```
Install the virtualenv.
```
$ poetry install
```