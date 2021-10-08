import wemulate.core.database.utils as dbutils
from wemulate.core.database.models import ConnectionModel, LogicalInterfaceModel
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
    physical_interface1_name: str = dbutils.get_physical_interface_by_logical_name(
        first_logical_interface
    ).physical_name
    physical_interface2_name: str = dbutils.get_physical_interface_by_logical_name(
        second_logical_interface
    ).physical_name
    return physical_interface1_name, physical_interface2_name


def get_logical_interface_by_name(
    logical_interface_name: str,
) -> Optional[LogicalInterfaceModel]:
    """
    Return the logical interface object for a given name

    Args:
        logical_interface_name: Logical interface name.

    Returns:
        Returns a logical interface object.
    """
    return dbutils.get_logical_interface_by_name(logical_interface_name)


def connection_exists_in_db(connection_name: str) -> bool:
    """
    Returns a true if a connection exists in the database

    Args:
        connection_name: Connection name.

    Returns:
        Returns a boolean.
    """
    return dbutils.connection_exists(connection_name)


def get_connection_by_name(connection_name: str) -> ConnectionModel:
    """
    Returns a a connection object for a connection name.

    Args:
        connection_name: Connection name.

    Returns:
        Returns a connection object.
    """
    return dbutils.get_connection_by_name(connection_name)


def get_connection_by_id(connection_id: int) -> ConnectionModel:
    """
    Returns a a connection object by its unique id.

    Args:
        connection_id: Connection id.

    Returns:
        Returns a connection object.
    """
    return dbutils.get_connection_by_id(connection_id)


def get_logical_interface_by_id(
    logical_interface_id: int,
) -> LogicalInterfaceModel:
    """
    Returns the logical interface object for the logical interface id.

    Args:
        logical_interface_id: The unique identifier for the specific logical interface.

    Returns:
        Returns a logical interface object.
    """
    return dbutils.get_logical_interface_by_id(logical_interface_id)


def get_logical_interface_by_physical_name(
    physical_interface_name: str,
) -> LogicalInterfaceModel:
    """
    Returns the logical interface object for a physical interface name.

    Args:
        physical_interface_name: Name of the physical interface.

    Returns:
        Returns a logical interface object.
    """
    return dbutils.get_logical_interface_by_physical_name(physical_interface_name)


def get_connection_list() -> List[ConnectionModel]:
    """
    Returns all existing connection objects as a list.

    Returns:
        Returns a list of connection objects.
    """
    return dbutils.get_connection_list()
