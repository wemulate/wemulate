from wemulate.core.database.decorators import use_db_session
from wemulate.core.exc import WEmulateValidationError
from wemulate.core.database.session import db_session
from wemulate.core.database.models import (
    DEFAULT_PARAMETERS,
    ProfileModel,
    ConnectionModel,
    InterfaceModel,
    LogicalInterfaceModel,
    DeviceModel,
    ParameterModel,
)


@use_db_session
def _get_interface_by_name(interface_name):
    return session.query(InterfaceModel).filter_by(physical_name=interface_name).first()


@use_db_session
def _get_specific_parameter_for_connection_id(connection_id, parameter):
    return (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .filter(ParameterModel.parameter_name == parameter)
        .first()
    )


@use_db_session
def _create_parameter(parameter_name, value, connection_id):
    parameter = ParameterModel(parameter_name, value, connection_id)
    session.add(parameter)


@use_db_session
def _update_parameter(parameter, value):
    if parameter.value == value:
        return False
    parameter.value = value
    session.add(parameter)
    session.commit()


@use_db_session
def _delete_all_connections():
    session.query(ConnectionModel).delete()
    session.commit()


@use_db_session
def _delete_all_parameters():
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
def get_device(device_id):
    return session.query(DeviceModel).filter_by(device_id=device_id).first()


@use_db_session
def get_active_profile(device):
    return session.query(ProfileModel).filter_by(belongs_to_device=device).first()


@use_db_session
def get_logical_interface(logical_interface_id):
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_interface_id=logical_interface_id)
        .first()
    )


@use_db_session
def get_logical_interface_by_name(logical_interface_name):
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_name=logical_interface_name)
        .first()
    )


@use_db_session
def get_logical_interface_for_physical_name(physical_interface_name):
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
def get_physical_interface_for_logical_name(logical_interface_name):
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
def get_physical_interface_for_logical_id(logical_interface_id):
    return (
        session.query(InterfaceModel)
        .filter_by(has_logical_interface_id=logical_interface_id)
        .first()
    )


@use_db_session
def get_connection_list():
    return session.query(ConnectionModel).all()


@use_db_session
def get_connection(connection_name):
    return (
        session.query(ConnectionModel)
        .filter(ConnectionModel.connection_name == connection_name)
        .first()
    )


@use_db_session
def get_specific_parameter_value_for_connection_id(connection_id, parameter):
    parameter_object = (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .filter(ParameterModel.parameter_name == parameter)
        .first()
    )
    if not parameter_object:
        return DEFAULT_PARAMETERS[parameter]
    return parameter_object.value


@use_db_session
def get_all_parameters_for_connection_id(connection_id):
    return (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .all()
    )


@use_db_session
def create_connection(
    connection_name, logical_interface1, logical_interface2, active_device_profile
):
    connection = ConnectionModel(
        connection_name,
        logical_interface1.logical_interface_id,
        logical_interface2.logical_interface_id,
        active_device_profile.profile_id,
    )
    session.add(connection)


def delete_all_parameter_on_connection(connection_id):
    parameters = get_all_parameters_for_connection_id(connection_id)
    for parameter in parameters:
        delete_parameter(parameter)


@use_db_session
def create_or_update_parameter(connection_id, parameter_value, value):
    parameter = _get_specific_parameter_for_connection_id(
        connection_id, parameter_value
    )
    if parameter:
        _update_parameter(parameter, value)
    else:
        _create_parameter(parameter_value, value, connection_id)


@use_db_session
def delete_parameter(parameter):
    session.delete(parameter)
    session.commit()


@use_db_session
def delete_parameter_on_connection_id(connection_id, parameter_name):
    parameter = _get_specific_parameter_for_connection_id(connection_id, parameter_name)
    session.delete(parameter)
    session.commit()


@use_db_session
def delete_connection_by_name(connection_name):
    connection = (
        session.query(ConnectionModel)
        .filter_by(connection_name=connection_name)
        .first()
    )
    session.delete(connection)
    session.commit()


@use_db_session
def delete_present_connection():
    connection_list = ConnectionModel.query.all()
    for connection in connection_list:
        session.delete(connection)
    session.commit()


def reset_all():
    _delete_all_parameters()
    _delete_all_connections()
