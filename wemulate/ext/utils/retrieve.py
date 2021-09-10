from wemulate.core.database.models import ConnectionModel, LogicalInterfaceModel
import wemulate.core.database.utils as dbutils
from typing import List, Optional, Tuple


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


def get_logical_interface_by_name(
    logical_interface_name: str,
) -> Optional[LogicalInterfaceModel]:
    return dbutils.get_logical_interface_by_name(logical_interface_name)


def connection_exists_in_db(connection_name: str) -> bool:
    return dbutils.connection_exists(connection_name)


def get_connection(connection_name: str) -> ConnectionModel:
    return dbutils.get_connection(connection_name)


def get_logical_interface_for_physical_name(
    physical_interface_name: str,
) -> LogicalInterfaceModel:
    return dbutils.get_logical_interface_for_physical_name(physical_interface_name)


def get_connection_list() -> List[ConnectionModel]:
    return dbutils.get_connection_list()
