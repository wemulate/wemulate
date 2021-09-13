.. _install:

Installation of WEmulate
#########################

This part of the documentation covers the installation of WEmulate.


Requirements
*************
In order to use WEmulate to influence traffic at least the following requirements should be fullfilled:

* At least 2 network interfaces for ``LAN-A`` and ``LAN-B``
* Ubuntu installed


Install with bash
**************************
To install WEmulate with bash, simply run this simple command in your terminal of choice::

    $ sh -c "$(curl -fsSL https://github.com/wemulate/wemulate/blob/main/install/install.sh)"


Install from source
**************************
You can also install WEmulate from source, please follow the instructions below:

* Install all dependencies:

.. code-block:: console

    $ sudo apt install --yes python3 python3-pip 

* Create a new configuration file: ``/etc/wemulate/wemulate.yml``

.. code-block:: console

    ---
    wemulate:
        management_interfaces:
            - eth0
        db_location: /etc/wemulate/wemulate.db

* Clone the repository

.. code-block:: console

    $ git clone https://github.com/wemulate/wemulate

* Install WEmulate

.. code-block:: console

    $ cd wemulate
    $ pip install -r requirements.txt
