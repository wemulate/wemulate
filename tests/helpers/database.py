import pytest
from sqlalchemy.orm.session import Session
from wemulate.core.database.session import database_engine
from wemulate.core.database.models import (
    ProfileModel,
    DeviceModel,
    LogicalInterfaceModel,
    InterfaceModel,
    ManagementInterfaceModel,
    Base,
    BANDWIDTH,
    DELAY,
    PACKET_LOSS,
    JITTER,
    DUPLICATION,
    CORRUPTION,
    INCOMING,
    OUTGOING,
)
from wemulate.core.database.decorators import use_db_session
from wemulate.core.database import utils as dbutils


def _pre_setup_mgmt_interfaces(session: Session) -> None:
    mgmt_interfaces = ["ens2", "ens3"]
    for mgmt in mgmt_interfaces:
        session.add(ManagementInterfaceModel(mgmt))


def _pre_setup_profile(session: Session) -> None:
    session.add(ProfileModel("default"))


def _pre_setup_device(session: Session) -> None:
    session.add(DeviceModel("wemulate", 1))


def _pre_setup_interfaces(session: Session) -> None:
    count = 0
    logical_interfaces = [
        ("LAN-A", "ens4"),
        ("LAN-B", "ens5"),
        ("LAN-C", "ens6"),
        ("LAN-D", "ens7"),
    ]
    for logic, physic in logical_interfaces:
        session.add(LogicalInterfaceModel(logic))
        session.add(InterfaceModel(physic, 1, count + 1))
        count += 1


@use_db_session
def _pre_setup_test_database(session: Session) -> None:
    """
    Initialize a test database with the following parameters:

    ProfileName: default
    Hostname: wemulate
    Physical Interfaces: [ens2, ens3, ens4, ens5, ens6, ens7]
    Mgmt Interfaces: [ens2, ens3]
    Logical Interfaces: [LAN-A, LAN-B, LAN-C, LAN-D]

    Returns:
        None
    """
    _pre_setup_mgmt_interfaces(session)
    _pre_setup_profile(session)
    _pre_setup_device(session)
    _pre_setup_interfaces(session)


@use_db_session
def _cleanup_test_database(session: Session) -> None:
    Base.metadata.drop_all(database_engine)


@pytest.fixture()
def db_test_setup():
    _pre_setup_test_database()

    yield

    _cleanup_test_database()


def create_one_connection():
    """
    Creates one connection:

    test: LAN-A to LAN-B
        delay: 10 incoming
        jitter: 20 outgoing
    """
    device: DeviceModel = dbutils.get_device()
    profile: ProfileModel = dbutils.get_active_profile(device)
    log1: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(1)
    log2: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(2)
    dbutils.create_connection("test", log1, log2, profile)
    dbutils.create_or_update_parameter(1, DELAY, 10, INCOMING)
    dbutils.create_or_update_parameter(1, JITTER, 20, OUTGOING)


def create_two_connections():
    """
    Creates two connections:

    test1: LAN-A to LAN-B
    test2: LAN-C to LAN-D
    """
    device: DeviceModel = dbutils.get_device()
    profile: ProfileModel = dbutils.get_active_profile(device)
    log1: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(1)
    log2: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(2)
    log3: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(3)
    log4: LogicalInterfaceModel = dbutils.get_logical_interface_by_id(4)
    dbutils.create_connection("test1", log1, log2, profile)
    dbutils.create_connection("test2", log3, log4, profile)
