from typing import List, Optional

import netifaces

import wemulate.core.database.utils as dbutils
from wemulate.core.exc import WEmulateExecutionError, WemulateMgmtInterfaceError
from wemulate.ext.utils.reset import reset_device


def _interface_present_on_device(interface_name: str) -> bool:
    return interface_name in get_all_interfaces_on_device()


def check_if_mgmt_interface_set() -> bool:
    if get_mgmt_interfaces():
        return True
    raise WEmulateExecutionError(
        "There is no management interface set in the config/database!"
    )
    # @TODO: check ConfigController to add mgmt interfaces
    # @TODO: check if execution works if any mgmt interface


def get_interface_ip(interface: str) -> Optional[str]:
    """
    Returns the ip address of an interface.

    Args:
        interface: Name of the interface.

    Returns:
        Returns the ip address as string.
    """
    if netifaces.AF_INET in netifaces.ifaddresses(interface):
        return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["addr"]
    else:
        "N/A"


def get_interface_mac_address(interface: str) -> str:
    """
    Returns the mac address of an interface.

    Args:
        interface: Name of the interface.

    Returns:
        Returns the mac address as string.
    """
    return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]


def get_mgmt_interfaces() -> List[str]:
    """
    Returns all management interfaces saved in the database.

    Returns:
        Returns the management interfaces as list of strings.
    """
    return [
        mgmt_interface.interface_name
        for mgmt_interface in dbutils.get_mgmt_interfaces()
    ]


def get_all_interfaces_on_device() -> List[str]:
    """
    Returns all interfaces on the device.

    Returns:
        Returns a list of interfaces.
    """
    return [name for name in netifaces.interfaces() if name.startswith(("eth", "en"))]


def add_mgmt_interface(interface_name: str) -> None:
    """
    Adds an interface as management interfaces.

    Args:
        interface_name: Name of the interface

    Returns:
        None
    """
    if _interface_present_on_device(interface_name):
        dbutils.create_mgmt_interface(interface_name)
    else:
        raise WemulateMgmtInterfaceError(interface_name)


def reset_mgmt_interfaces() -> None:
    """
    Resets all management interfaces and all linked settings.

    Returns:
        None
    """
    reset_device()
    dbutils.delete_logical_interfaces()
    dbutils.delete_mgmt_interfaces()
    dbutils.delete_interfaces()


def get_non_mgmt_interfaces() -> List[str]:
    """
    Returns all interfaces which usable to connect different devices (all non-mgmt interfaces).

    Returns:
        Returns the interfaces as list of strings.
    """
    return [
        interface_name
        for interface_name in get_all_interfaces_on_device()
        if interface_name not in get_mgmt_interfaces()
    ]
