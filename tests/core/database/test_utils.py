from typing import List
from tests.helpers.database import (
    db_test_setup,
    create_two_connections,
    create_one_connection,
)
from wemulate.core.database import utils as dbutils
from wemulate.core.database.models import (
    ProfileModel,
    ManagementInterfaceModel,
    LogicalInterfaceModel,
    DeviceModel,
    InterfaceModel,
    ConnectionModel,
    BANDWIDTH,
    DELAY,
    INCOMING,
)


def test_get_device(db_test_setup):
    device: DeviceModel = dbutils.get_device()
    assert device.device_id == 1
    assert device.device_name == "wemulate"


def test_get_active_profile(db_test_setup):
    device: DeviceModel = dbutils.get_device()
    profile: ProfileModel = dbutils.get_active_profile(device)
    assert profile.profile_id == 1
    assert profile.profile_name == "default"


def test_get_logical_interface_by_id(db_test_setup):
    logical_interface: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(1)
    assert logical_interface.logical_interface_id == 1
    assert logical_interface.logical_name == "LAN-A"


def test_get_logical_interface_by_name(db_test_setup):
    logical_interface: LogicalInterfaceModel = dbutils.get_logical_interface_by_name(
        "LAN-A"
    )
    assert logical_interface.logical_interface_id == 1
    assert logical_interface.logical_name == "LAN-A"


def test_get_logical_interface_by_physical_name(db_test_setup):
    logical_interface: LogicalInterfaceModel = (
        dbutils.get_logical_interface_by_physical_name("ens4")
    )
    assert logical_interface.logical_interface_id == 1
    assert logical_interface.logical_name == "LAN-A"


def test_get_physical_interface_by_logical_interface_id(db_test_setup):
    physical_interface: InterfaceModel = (
        dbutils.get_physical_interface_by_logical_interface_id(1)
    )
    assert physical_interface.interface_id == 1
    assert physical_interface.physical_name == "ens4"


def test_get_physical_interface_by_logical_name(db_test_setup):
    physical_interface: InterfaceModel = dbutils.get_physical_interface_by_logical_name(
        "LAN-A"
    )
    assert physical_interface.interface_id == 1
    assert physical_interface.physical_name == "ens4"


def test_get_connection_list(db_test_setup):
    create_two_connections()
    connection_list: List[ConnectionModel] = dbutils.get_connection_list()
    assert len(connection_list) == 2


def test_get_connection_by_id(db_test_setup):
    create_one_connection()
    connection: ConnectionModel = dbutils.get_connection_by_id(1)
    assert connection.connection_id == 1
    assert connection.connection_name == "test"
    assert connection.first_logical_interface_id == 1
    assert connection.second_logical_interface_id == 2


def test_get_connection_by_name(db_test_setup):
    create_one_connection()
    connection: ConnectionModel = dbutils.get_connection_by_name("test")
    assert connection.connection_id == 1
    assert connection.connection_name == "test"
    assert connection.first_logical_interface_id == 1
    assert connection.second_logical_interface_id == 2


def test_create_connection(db_test_setup):
    device: DeviceModel = dbutils.get_device()
    profile: ProfileModel = dbutils.get_active_profile(device)
    log1: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(1)
    log2: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(2)
    dbutils.create_connection("test99", log1, log2, profile)

    connection: ConnectionModel = dbutils.get_connection_by_name("test99")
    assert connection.connection_name == "test99"
    assert connection.first_logical_interface_id == 1
    assert connection.second_logical_interface_id == 2


def test_delete_all_parameter_on_connection(db_test_setup):
    create_one_connection()
    dbutils.delete_all_parameter_on_connection(1)
    connection: ConnectionModel = dbutils.get_connection_by_id(1)
    assert connection.parameters == []


def test_create_or_update_parameter(db_test_setup):
    create_one_connection()
    dbutils.create_or_update_parameter(1, DELAY, 20, INCOMING)
    dbutils.create_or_update_parameter(1, BANDWIDTH, 100, INCOMING)
    connection: ConnectionModel = dbutils.get_connection_by_id(1)
    for param in connection.parameters:
        if param.parameter_name == DELAY:
            assert param.value == 20
            assert param.direction == INCOMING
        if param.parameter_name == BANDWIDTH:
            assert param.value == 100
            assert param.direction == INCOMING


def test_delete_parameter_on_connection_id(db_test_setup):
    create_one_connection()
    dbutils.delete_parameter_on_connection_id(1, DELAY, INCOMING)
    connection: ConnectionModel = dbutils.get_connection_by_id(1)
    for param in connection.parameters:
        if param.parameter_name == DELAY:
            assert False


def test_delete_connection_by_name(db_test_setup):
    create_one_connection()
    dbutils.delete_connection_by_name("test")
    assert dbutils.get_connection_by_name("test") == None


def test_reset_all_connections(db_test_setup):
    create_two_connections()
    dbutils.reset_all_connections()
    connection_list: List[ConnectionModel] = dbutils.get_connection_list()
    assert connection_list == []


def test_get_mgmt_interfaces(db_test_setup):
    mgmt_interfaces: List[ManagementInterfaceModel] = dbutils.get_mgmt_interfaces()
    count = 2
    dbcount = 1
    for mgmt in mgmt_interfaces:
        assert mgmt.interface_name == f"ens{count}"
        assert mgmt.management_interface_id == dbcount
        count += 1
        dbcount += 1


def test_create_mgmt_interfaces(db_test_setup):
    new_mgmt_name = "ens99"
    dbutils.create_mgmt_interface(new_mgmt_name)
    mgmt_interfaces: List[ManagementInterfaceModel] = dbutils.get_mgmt_interfaces()
    assert mgmt_interfaces[len(mgmt_interfaces) - 1].interface_name == new_mgmt_name


def test_get_logical_interfaces(db_test_setup):
    logical_interfaces: List[LogicalInterfaceModel] = dbutils.get_logical_interfaces()
    assert len(logical_interfaces) == 4


def test_delete_logical_interfaces(db_test_setup):
    dbutils.delete_logical_interfaces()
    logical_interfaces: List[LogicalInterfaceModel] = dbutils.get_logical_interfaces()
    assert logical_interfaces == []


def test_delete_mgmt_intefaces(db_test_setup):
    dbutils.delete_mgmt_interfaces()
    mgmt_interfaces: List[ManagementInterfaceModel] = dbutils.get_mgmt_interfaces()
    assert mgmt_interfaces == []


def test_delete_interfaces(db_test_setup):
    dbutils.delete_interfaces()
    interfaces: List[InterfaceModel] = dbutils.get_interfaces()
    assert interfaces == []


def test_get_interfaces(db_test_setup):
    interfaces: List[InterfaceModel] = dbutils.get_interfaces()
    count = 4
    dbcount = 1
    for int in interfaces:
        assert int.interface_id == dbcount
        assert int.physical_name == f"ens{count}"
        dbcount += 1
        count += 1
