from typing import Dict, List
from wemulate.core.database.decorators import use_db_session
from wemulate.core.database.models import (
    ProfileModel,
    ConnectionModel,
    InterfaceModel,
    LogicalInterfaceModel,
    DeviceModel,
    ParameterModel,
)


@use_db_session
def _get_interface_by_name(interface_name) -> InterfaceModel:
    return session.query(InterfaceModel).filter_by(physical_name=interface_name).first()


@use_db_session
def _get_specific_parameter_for_connection_id(
    connection_id, parameter
) -> ParameterModel:
    return (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .filter(ParameterModel.parameter_name == parameter)
        .first()
    )


@use_db_session
def _create_parameter(parameter_name, value, connection_id) -> None:
    parameter = ParameterModel(parameter_name, value, connection_id)
    session.add(parameter)


@use_db_session
def _update_parameter(parameter, value) -> None:
    if parameter.value == value:
        return False
    parameter.value = value
    session.add(parameter)


@use_db_session
def _delete_all_connections() -> None:
    session.query(ConnectionModel).delete()
    session.commit()


@use_db_session
def _delete_all_parameters() -> None:
    session.query(ParameterModel).delete()
    session.commit()


@use_db_session
def connection_exists(connection_name: str) -> bool:
    if (
        not session.query(ConnectionModel)
        .filter_by(connection_name=connection_name)
        .first()
    ):
        return False
    return True


@use_db_session
def get_device(device_id) -> DeviceModel:
    return session.query(DeviceModel).filter_by(device_id=device_id).first()


@use_db_session
def get_active_profile(device) -> ProfileModel:
    return session.query(ProfileModel).filter_by(belongs_to_device=device).first()


@use_db_session
def get_logical_interface_by_name(logical_interface_name) -> LogicalInterfaceModel:
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_name=logical_interface_name)
        .first()
    )


@use_db_session
def get_logical_interface_for_physical_name(
    physical_interface_name,
) -> LogicalInterfaceModel:
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(
            logical_interface_id=_get_interface_by_name(
                physical_interface_name
            ).has_logical_interface_id
        )
        .first()
    )


@use_db_session
def get_physical_interface_for_logical_name(logical_interface_name) -> InterfaceModel:
    logical_interface = (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_name=logical_interface_name)
        .first()
    )
    return (
        session.query(InterfaceModel)
        .filter_by(has_logical_interface_id=logical_interface.logical_interface_id)
        .first()
    )


@use_db_session
def get_physical_interface_for_logical_id(logical_interface_id) -> InterfaceModel:
    return (
        session.query(InterfaceModel)
        .filter_by(has_logical_interface_id=logical_interface_id)
        .first()
    )


@use_db_session
def get_connection_list() -> List[ConnectionModel]:
    return session.query(ConnectionModel).all()


@use_db_session
def get_connection(connection_name) -> ConnectionModel:
    return (
        session.query(ConnectionModel)
        .filter(ConnectionModel.connection_name == connection_name)
        .first()
    )


@use_db_session
def create_connection(
    connection_name, logical_interface1, logical_interface2, active_device_profile
) -> None:
    connection = ConnectionModel(
        connection_name,
        logical_interface1.logical_interface_id,
        logical_interface2.logical_interface_id,
        active_device_profile.profile_id,
    )
    session.add(connection)


@use_db_session
def delete_all_parameter_on_connection(connection_id) -> None:
    (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .delete()
    )


@use_db_session
def create_or_update_parameter(connection_id, parameter_value, value) -> None:
    parameter = _get_specific_parameter_for_connection_id(
        connection_id, parameter_value
    )
    if parameter:
        _update_parameter(parameter, value)
    else:
        _create_parameter(parameter_value, value, connection_id)


@use_db_session
def delete_parameter_on_connection_id(connection_id, parameter_name) -> None:
    parameter = _get_specific_parameter_for_connection_id(connection_id, parameter_name)
    session.delete(parameter)


@use_db_session
def delete_connection_by_name(connection_name) -> None:
    connection = (
        session.query(ConnectionModel)
        .filter_by(connection_name=connection_name)
        .first()
    )
    session.delete(connection)


def reset_all_connections() -> None:
    _delete_all_parameters()
    _delete_all_connections()
