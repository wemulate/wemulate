from wemulate.core.database import session
from wemulate.core.database.models import (
    ProfileModel,
    ConnectionModel,
    InterfaceModel,
    LogicalInterfaceModel,
    DeviceModel,
    ParameterModel,
)


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


def get_logical_interface_list():
    return session.query(LogicalInterfaceModel).all()


def get_connection_list():
    return session.query(ConnectionModel).all()


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
    session.commit()


def create_parameter(parameter_name, value, connection_id):
    parameter = ParameterModel(parameter_name, value, connection_id)
    session.add(parameter)
    session.commit()


def create_interface(physical_name, device_id, logical_interface_id):
    interface = InterfaceModel(physical_name, device_id, logical_interface_id)
    db.session.add(interface)
    db.session.flush()
    return interface


def update_parameter(parameter, value):
    if parameter.value == value:
        return False
    parameter.value = value
    db.session.add(parameter)
    db.session.flush()
    return True


def update_connection(connection, connection_name):
    if connection.connection_name == connection_name:
        return False
    connection.connection_name = connection_name
    db.session.add(connection)
    db.session.flush()
    return True


def delete_connection(connection):
    db.session.delete(connection)
    db.session.flush()


def create_logical_interfaces():
    for character in list(string.ascii_uppercase):
        logical_interface = LogicalInterfaceModel("LAN-" + character)
        db.session.add(logical_interface)
    db.session.flush()


def delete_present_connection():
    try:
        connection_list = ConnectionModel.query.all()
        for connection in connection_list:
            db.session.delete(connection)
        db.session.commit()
    except:
        print("Flushing Connection Table")
