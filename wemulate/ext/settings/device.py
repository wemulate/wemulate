import netifaces
from typing import List
import wemulate.ext.settings.config as config


def get_interface_ip(interface: str) -> str:
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
    Returns all management interfaces defined in the configuration as list.

    Returns:
        Returns the management interfaces as list of strings.
    """
    return config.get_config()["wemulate"]["management_interfaces"]


def get_interfaces() -> List[str]:
    """
    Returns all interfaces which usable to connect different devices.

    Returns:
        Returns the interfaces as list of strings.
    """
    return [
        name
        for name in netifaces.interfaces()
        if name.startswith(("eth", "en"))
        and name not in config.get_config()["wemulate"]["management_interfaces"]
    ]
