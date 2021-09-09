import wemulate.core.database.utils as dbutils
from typing import Dict, List, Optional, Tuple


def get_physical_interface_names(
    first_logical_interface: str, second_logical_interface: str
) -> Tuple[str, str]:
    """
    Get the physical interface names for the logical interface names.

    Args:
        first_logical_interface: First logical interface name.
        second_logical_interface: Second logical interface name.

    Returns:
        Tuple of strings.
    """
    physical_interface1_name: str = dbutils.get_physical_interface_for_logical_name(
        first_logical_interface
    ).physical_name
    physical_interface2_name: str = dbutils.get_physical_interface_for_logical_name(
        second_logical_interface
    ).physical_name
    return physical_interface1_name, physical_interface2_name
