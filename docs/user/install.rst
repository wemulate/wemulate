.. _install:

Installation of WEmulate
#########################

This part of the documentation covers the installation of WEmulate.


Requirements
*************
In order to use WEmulate to influence traffic at least the following requirements should be fullfilled:

* At least 3 network interfaces for ``LAN-A``, ``LAN-B`` and the management interface.
* Ubuntu installed


Install with bash
**************************
To install WEmulate with bash, simply run this simple command in your terminal of choice::

    $ bash -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)"

There are different arguments available in order to enhance the installation experience:

* ``-h`` Prints the help message
* ``-f`` Skip the confirmation prompt during installation
* ``-i <int1,int2>`` List of interfaces which should be used as management interfaces
* ``-a`` Installs the api module
* ``-v`` Installs the frontend module

If you want to use some arguments directly with the script, you can do so by adding them to the command::

    $ curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh | bash -s -- -a -v -i ens2,ens3 -f


Install from source
**************************
You can also install WEmulate from source, please follow the instructions below:

* Install poetry (see `here <https://python-poetry.org/docs/#installation>`_ for more information)

* Install all dependencies:

.. code-block:: console

    $ sudo apt install --yes python3 python3-pip 

* Clone the repository

.. code-block:: console

    $ git clone https://github.com/wemulate/wemulate

* Install WEmulate

.. code-block:: console

    $ cd wemulate
    $ poetry install

* Configure the management interfaces

.. code-block:: console

    $ wemulate config set -m ens2