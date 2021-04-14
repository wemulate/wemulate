import string
from wemulate.core.exc import WEmulateValidationError
from wemulate.core.database import session
from wemulate.core.database.models import (
    ProfileModel,
    ConnectionModel,
    InterfaceModel,
    LogicalInterfaceModel,
    DeviceModel,
    ParameterModel,
)
from sqlalchemy.exc import IntegrityError as AlchemyIntegrityError


def connection_exists(connection_name: str) -> bool:
    if (
        not session.query(ConnectionModel)
        .filter_by(connection_name=connection_name)
        .first()
    ):
        return False
    return True


def get_device(device_id):
    return session.query(DeviceModel).filter_by(device_id=device_id).first()


def get_device_by_name(device_name):
    return session.query(DeviceModel).filter_by(device_name=device_name).first()


def is_device_present(device_name):
    return (
        session.query(DeviceModel).filter_by(device_name=device_name).first()
        is not None
    )


def get_device_list():
    return session.query(DeviceModel).all()


def get_active_profile(device):
    return session.query(ProfileModel).filter_by(belongs_to_device=device).first()


def get_all_interfaces(device):
    return (
        session.query(InterfaceModel)
        .filter_by(belongs_to_device_id=device.device_id)
        .all()
    )


def get_interface_by_name(interface_name):
    return session.query(InterfaceModel).filter_by(physical_name=interface_name).first()


def get_logical_interface(logical_interface_id):
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_interface_id=logical_interface_id)
        .first()
    )


def get_logical_interface_by_name(logical_interface_name):
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_name=logical_interface_name)
        .first()
    )


def get_logical_interface_for_physical_name(physical_interface_name):
    return (
        session.query(LogicalInterfaceModel)
        .filter_by(
            logical_interface_id=get_interface_by_name(
                physical_interface_name
            ).has_logical_interface_id
        )
        .first()
    )


def get_physical_interface_for_logical_name(logical_interface_name):
    logical_interface = (
        session.query(LogicalInterfaceModel)
        .filter_by(logical_name=logical_interface_name)
        .first()
    )
    return session.query(InterfaceModel).filter_by(
        has_logical_interface_id=logical_interface.logical_interface_id
    )


def get_logical_interface_list():
    return session.query(LogicalInterfaceModel).all()


def get_connection_list():
    return session.query(ConnectionModel).all()


def get_connection(connection_name):
    return (
        session.query(ConnectionModel)
        .filter(ConnectionModel.connection_name == connection_name)
        .first()
    )


def get_specific_parameter_for_connection_id(connection_id, parameter):
    return (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .filter(ParameterModel.parameter_name == parameter)
        .first()
    )


def get_all_parameters_for_connection_id(connection_id):
    return (
        session.query(ParameterModel)
        .filter(ParameterModel.belongs_to_connection_id == connection_id)
        .all()
    )


# def create_profile(device_name):
#     profile = ProfileModel("default_" + device_name)
#     db.session.add(profile)
#     db.session.flush()
#     return profile


# def create_device(device_name, profile_id, management_ip):
#     if management_ip is None:
#         device = DeviceModel(device_name, profile_id)
#     else:
#         device = DeviceModel(device_name, profile_id, management_ip)
#     db.session.add(device)
#     db.session.flush()
#     return device


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
    try:
        session.commit()
    except AlchemyIntegrityError as e:
        splitting = e.args[0].split(
            "(sqlite3.IntegrityError) UNIQUE constraint failed: connection.", 1
        )[1]
        raise WEmulateValidationError(message=splitting)


def create_parameter(parameter_name, value, connection_id):
    parameter = ParameterModel(parameter_name, value, connection_id)
    session.add(parameter)
    session.commit()


def delete_all_parameter_on_connection(connection_id):
    parameters = get_all_parameters_for_connection_id(connection_id)
    for param in parameters:
        delete_parameter(param)


def create_or_update_parameter(connection_id, parameter_value, value):
    parameter = get_specific_parameter_for_connection_id(connection_id, parameter_value)
    if parameter:
        update_parameter(parameter, value)
    else:
        create_parameter(parameter_value, value, connection_id)


def create_interface(physical_name, device_id, logical_interface_id):
    interface = InterfaceModel(physical_name, device_id, logical_interface_id)
    session.add(interface)
    session.commit()


def update_parameter(parameter, value):
    if parameter.value == value:
        return False
    parameter.value = value
    session.add(parameter)
    session.commit()


def delete_parameter(parameter):
    session.delete(parameter)
    session.commit()


def update_connection(connection, connection_name):
    if connection.connection_name == connection_name:
        return False
    connection.connection_name = connection_name
    session.add(connection)
    session.commit()


def delete_connection(connection):
    session.delete(connection)
    session.commit()


def delete_connection_by_name(connection_name):
    connection = (
        session.query(ConnectionModel)
        .filter_by(connection_name=connection_name)
        .first()
    )
    session.delete(connection)
    session.commit()


# def create_logical_interfaces():
#     for character in list(string.ascii_uppercase):
#         logical_interface = LogicalInterfaceModel("LAN-" + character)
#         session.add(logical_interface)
#     session.commit()


def delete_present_connection():
    connection_list = ConnectionModel.query.all()
    for connection in connection_list:
        session.delete(connection)
    session.commit()


def delete_all_connections():
    session.query(ConnectionModel).delete()
    session.commit()


def delete_all_parameters():
    session.query(ParameterModel).delete()
    session.commit()


def reset_all():
    delete_all_parameters()
    delete_all_connections()