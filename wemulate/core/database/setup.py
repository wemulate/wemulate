import socket, string
from wemulate.utils.settings import get_interfaces, get_mgmt_interfaces
from wemulate.core.database import session
from wemulate.core.database.models import (
    ProfileModel,
    DeviceModel,
    LogicalInterfaceModel,
    InterfaceModel,
)


def pre_setup_profile(app):
    if not session.query(ProfileModel).filter_by(profile_name="default").first():
        session.add(ProfileModel("default"))
        session.commit()


def pre_setup_device(app):
    hostname = socket.gethostname()
    if not session.query(DeviceModel).filter_by(device_name=hostname).first():
        session.add(DeviceModel(hostname, 1, get_mgmt_interfaces()[0]))
        session.commit()


def pre_setup_logical_interfaces(ascii_index):
    if (
        not session.query(LogicalInterfaceModel)
        .filter_by(logical_name="LAN-" + string.ascii_uppercase[ascii_index])
        .first()
    ):
        session.add(LogicalInterfaceModel("LAN-" + string.ascii_uppercase[ascii_index]))
        session.commit()


def pre_setup_interfaces(app):
    count = 0
    for int in get_interfaces():
        if not session.query(InterfaceModel).filter_by(physical_name=int).first():
            pre_setup_logical_interfaces(count)
            session.add(InterfaceModel(int, 1, count + 1))
            session.commit()
            ++count