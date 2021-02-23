# A modern WAN Emulator

## Installation

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run wemulate cli application

$ wemulate --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `WEmulate`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it wemulate --help
```

## Usage

### Command Tree
The commands are structured as follow:
```
show
    connection
        conn1
    connections
    interface
        eth0
    interfaces
    mgmt-interfaces
list
    connections
    interfaces
    mgmt-interfaces
add
    connection
        -n conn1 -i eth1,eth2
    parameter
        -n conn1 -b -j -d -l
set
    parameter
        -n conn1 -b -j -d -l
delete
    connection
        conn1
    parameter
        -n conn1 -b -j -d -l
reset
    connection
        conn1
    all
load
    -f
        ~/
save
    -f
        ~/
config
    mgmt-interfaces
        -n eth0 eth1
```