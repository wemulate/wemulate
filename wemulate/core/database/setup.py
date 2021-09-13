import socket, string
import wemulate.ext.settings as settings
from sqlalchemy.orm.session import Session
from wemulate.core.database.models import (
    ProfileModel,
    DeviceModel,
    LogicalInterfaceModel,
    InterfaceModel,
)
from wemulate.core.database.decorators import use_db_session


def _pre_setup_profile(session: Session) -> None:
    DEFAULT_PROFILE_NAME: str = "default"
    if (
        not session.query(ProfileModel)
        .filter_by(profile_name=DEFAULT_PROFILE_NAME)
        .first()
    ):
        session.add(ProfileModel(DEFAULT_PROFILE_NAME))


def _pre_setup_device(session: Session) -> None:
    hostname: str = socket.gethostname()
    PROFILE_ID: int = 1
    if not session.query(DeviceModel).filter_by(device_name=hostname).first():
        session.add(
            DeviceModel(hostname, PROFILE_ID, settings.get_mgmt_interfaces()[0])
        )


def _pre_setup_logical_interfaces(session: Session, ascii_index: int) -> None:
    if (
        not session.query(LogicalInterfaceModel)
        .filter_by(logical_name="LAN-" + string.ascii_uppercase[ascii_index])
        .first()
    ):
        session.add(LogicalInterfaceModel("LAN-" + string.ascii_uppercase[ascii_index]))


def _pre_setup_interfaces(session: Session) -> None:
    count: int = 0
    DEVICE_ID: int = 1
    for physical_interface in settings.get_interfaces():
        if (
            not session.query(InterfaceModel)
            .filter_by(physical_name=physical_interface)
            .first()
        ):
            _pre_setup_logical_interfaces(session, count)
            session.add(InterfaceModel(physical_interface, DEVICE_ID, count + 1))
            count += 1


@use_db_session
def pre_setup_database(session: Session) -> None:
    _pre_setup_profile(session)
    _pre_setup_device(session)
    _pre_setup_interfaces(session)
