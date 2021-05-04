[![Publish WEmulate package to PyPi](https://github.com/wemulate/wemulate/actions/workflows/publish-package.yml/badge.svg)](https://github.com/wemulate/wemulate/actions/workflows/publish-package.yml)
# WEmulate
**A modern WAN Emulator developed by the Institute for Networked Solutions**


## Installation

### Prerequisites
* Virtual machine or physical device with at least two interfaces
* Root permissions 

### Getting Started
Install wemulate cli application  
```bash
$ sh -c "$(curl -fsSL https://github.com/wemulate/wemulate/blob/main/install/install.sh)"
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
