[![CI](https://github.com/wemulate/wemulate/actions/workflows/test-python.yml/badge.svg)](https://github.com/wemulate/wemulate/actions/workflows/test-python.yml)
[![codecov](https://codecov.io/github/wemulate/wemulate/branch/main/graph/badge.svg?token=PCERPBMLFY)](https://codecov.io/github/wemulate/wemulate)
**A modern WAN Emulator developed by the Institute for Networked Solutions**
# WEmulate

Have a look at the [documentation](https://wemulate.github.io/wemulate) for detailed information.

## Installation

### Requirements
* At least two network interfaces for ``LAN-A`` and ``LAN-B``
* A third management interface if you would like to use the api and frontend module
* Ubuntu installed
* Root permissions

### Getting Started
To install only the WEmulate cli with bash, simply run this command in your terminal of choice:
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)"
```
There are different arguments available in order to enhance the installation experience:
```
-h               Prints the help message
-f               Skip the confirmation prompt during installation
-i <int1,int2>   List of interfaces which should be used as management interfaces
-a               Install the api module
-v               Install the frontend module
```
You can for example install the cli, api and frontend module together with one management interface with the following command:
```
curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh | bash -s -- -a -v -i ens2 -f
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

### Testing
In order to test WEmulate and to use an in-memory sqlite database, the following environment variable has to be set:
```
export WEMULATE_TESTING=true
```
Install the dev dependencies:
```
poetry install --with dev
```
The tests can then be executed with pytest.
```
poetry run pytest
```