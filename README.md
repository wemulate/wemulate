**A modern WAN Emulator developed by the Institute for Networked Solutions**
# WEmulate

Have a look at the [documentation](https://wemulate.github.io/wemulate) for detailed information.

## Installation

### Prerequisites
* Virtual machine or physical device with at least two interfaces
* Root permissions 

### Getting Started
Install wemulate cli application  
```bash
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)"
```

## Usage 
```bash
# Add a new connection
$ wemulate add connection -n connectionname -i LAN-A,LAN-B

# Delete a connection
$ wemulate delete connection -n connectionname

# Add parameters
$ wemulate add parameter -n connectionname -j 20 -d 40
```
