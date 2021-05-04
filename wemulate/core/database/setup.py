import socket, string
from wemulate.utils.settings import get_interfaces, get_mgmt_interfaces
from wemulate.core.database.session import session
from wemulate.core.database.models import (
    ProfileModel,
    DeviceModel,
    LogicalInterfaceModel,
    InterfaceModel,
)
from wemulate.core.database.decorators import rollback_if_necessary

@rollback_if_necessary
def _pre_setup_profile():
    DEFAULT_PROFILE_NAME = "default"
    if not session.query(ProfileModel).filter_by(profile_name=DEFAULT_PROFILE_NAME).first():
        session.add(ProfileModel(DEFAULT_PROFILE_NAME))
        session.commit()

@rollback_if_necessary
def _pre_setup_device():
    hostname = socket.gethostname()
    PROFILE_ID = 1
    if not session.query(DeviceModel).filter_by(device_name=hostname).first():
        session.add(DeviceModel(hostname, PROFILE_ID, get_mgmt_interfaces()[0]))
        session.commit()

@rollback_if_necessary
def _pre_setup_logical_interfaces(ascii_index):
    if (
        not session.query(LogicalInterfaceModel)
        .filter_by(logical_name="LAN-" + string.ascii_uppercase[ascii_index])
        .first()
    ):
        session.add(LogicalInterfaceModel("LAN-" + string.ascii_uppercase[ascii_index]))
        session.commit()

@rollback_if_necessary
def _pre_setup_interfaces() -> None:
    count : int = 0
    DEVICE_ID = 1
    for physical_interface in get_interfaces():
        if (
            not session.query(InterfaceModel)
            .filter_by(physical_name=physical_interface)
            .first()
        ):
            _pre_setup_logical_interfaces(count)
            session.add(InterfaceModel(physical_interface, DEVICE_ID, count + 1))
            session.commit()
            count += 1

def pre_setup_database() -> None:
    _pre_setup_profile()
    _pre_setup_device()
    _pre_setup_interfaces()
