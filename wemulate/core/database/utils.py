from typing import List, Optional
from sqlalchemy.orm.session import Session
from wemulate.core.database.decorators import use_db_session
from wemulate.core.database.models import (
    ProfileModel,
    ConnectionModel,
    InterfaceModel,
    LogicalInterfaceModel,
    DeviceModel,
    ParameterModel,
)


def _get_interface_by_name(
    session: Session,
    interface_name: str,
) -> Optional[InterfaceModel]:
    return session.query(InterfaceModel).filter_by(physical_name=interface_name).first()


@use_db_session
def _get_specific_parameter_by_connection_id(
    session: Session, connection_id: int, parameter_name: str
) -> Optional[ParameterModel]:
    return (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .filter(ParameterModel.parameter_name == parameter_name)
        .first()
    )


@use_db_session
def _create_parameter(
    session: Session, parameter_name: str, value: int, connection_id: int
) -> None:
    parameter: ParameterModel = ParameterModel(parameter_name, value, connection_id)
    session.add(parameter)


@use_db_session
def _update_parameter(session: Session, parameter, value) -> None:
    if parameter.value != value:
        parameter.value = value
        session.add(parameter)


@use_db_session
def _delete_all_connections(session: Session) -> None:
    session.query(ConnectionModel).delete()


@use_db_session
def _delete_all_parameters(session: Session) -> None:
    session.query(ParameterModel).delete()


@use_db_session
def connection_exists(session: Session, connection_name: str) -> bool:
    if (
        session.query(ConnectionModel)
        .filter_by(connection_name=connection_name)
        .first()
    ):
        return True
    return False


@use_db_session
def get_device(session: Session, device_id: int) -> Optional[DeviceModel]:
    return session.query(DeviceModel).filter_by(device_id=device_id).first()


@use_db_session
def get_active_profile(session: Session, device: DeviceModel) -> Optional[ProfileModel]:
    return session.query(ProfileModel).filter_by(belongs_to_device=device).first()


@use_db_session
def get_logical_interface_by_id(
    session: Session, logical_interface_id: int
) -> Optional[LogicalInterfaceModel]:
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_interface_id=logical_interface_id)
        .first()
    )


@use_db_session
def get_logical_interface_by_name(
    session: Session, logical_interface_name: str
) -> Optional[LogicalInterfaceModel]:
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_name=logical_interface_name)
        .first()
    )


@use_db_session
def get_logical_interface_by_physical_name(
    session: Session,
    physical_interface_name: str,
) -> Optional[LogicalInterfaceModel]:
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(
            logical_interface_id=_get_interface_by_name(
                session, physical_interface_name
            ).has_logical_interface_id
        )
        .first()
    )


@use_db_session
def get_physical_interface_by_logical_interface_id(
    session: Session, logical_interface_id: int
) -> Optional[InterfaceModel]:
    return (
        session.query(InterfaceModel)
        .filter_by(has_logical_interface_id=logical_interface_id)
        .first()
    )


@use_db_session
def get_physical_interface_by_logical_name(
    session: Session, logical_interface_name: str
) -> Optional[InterfaceModel]:
    logical_interface: Optional[LogicalInterfaceModel] = (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_name=logical_interface_name)
        .first()
    )
    if logical_interface:
        return (
            session.query(InterfaceModel)
            .filter_by(has_logical_interface_id=logical_interface.logical_interface_id)
            .first()
        )


@use_db_session
def get_connection_list(session: Session) -> List[ConnectionModel]:
    return session.query(ConnectionModel).all()


@use_db_session
def get_connection_by_id(
    session: Session, connection_id: int
) -> Optional[ConnectionModel]:
    return (
        session.query(ConnectionModel)
        .filter(ConnectionModel.connection_id == connection_id)
        .first()
    )


@use_db_session
def get_connection_by_name(
    session: Session, connection_name: str
) -> Optional[ConnectionModel]:
    return (
        session.query(ConnectionModel)
        .filter(ConnectionModel.connection_name == connection_name)
        .first()
    )


@use_db_session
def create_connection(
    session: Session,
    connection_name: str,
    logical_interface1: LogicalInterfaceModel,
    logical_interface2: LogicalInterfaceModel,
    active_device_profile: DeviceModel,
) -> None:
    connection: ConnectionModel = ConnectionModel(
        connection_name,
        logical_interface1.logical_interface_id,
        logical_interface2.logical_interface_id,
        active_device_profile.profile_id,
    )
    session.add(connection)


@use_db_session
def delete_all_parameter_on_connection(session: Session, connection_id: int) -> None:
    (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .delete()
    )


def create_or_update_parameter(
    connection_id: int, parameter_name: str, value: int
) -> None:
    parameter: Optional[ParameterModel] = _get_specific_parameter_by_connection_id(
        connection_id, parameter_name
    )
    if parameter:
        _update_parameter(parameter, value)
    else:
        _create_parameter(parameter_name, value, connection_id)


@use_db_session
def delete_parameter_on_connection_id(
    session: Session, connection_id: int, parameter_name: str
) -> None:
    parameter: Optional[ParameterModel] = _get_specific_parameter_by_connection_id(
        connection_id, parameter_name
    )
    if parameter:
        session.delete(parameter)


@use_db_session
def delete_connection_by_name(session: Session, connection_name: str) -> None:
    connection: Optional[ConnectionModel] = (
        session.query(ConnectionModel)
        .filter_by(connection_name=connection_name)
        .first()
    )
    if connection:
        session.delete(connection)


def reset_all_connections() -> None:
    _delete_all_parameters()
    _delete_all_connections()
