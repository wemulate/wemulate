import json
from typing import Dict, List

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from wemulate.core.database.session import database_engine


BANDWIDTH: str = "bandwidth"
DELAY: str = "delay"
PACKET_LOSS: str = "packet_loss"
JITTER: str = "jitter"
DUPLICATION: str = "duplication"
CORRUPTION: str = "corruption"
INCOMING: str = "incoming"
OUTGOING: str = "outgoing"

PARAMETERS: List[str] = [BANDWIDTH, DELAY, PACKET_LOSS, JITTER, DUPLICATION, CORRUPTION]

DEFAULT_PARAMETERS: Dict[str, int] = {
    BANDWIDTH: 0,
    DELAY: 0,
    PACKET_LOSS: 0,
    JITTER: 0,
}

Base = declarative_base()


class ProfileModel(Base):
    __tablename__ = "profile"
    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    profile_name = Column(String(50))
    connections = relationship(
        "ConnectionModel",
        backref="belongs_to_profile",
        lazy=False,
        cascade="delete",
        order_by="asc(ConnectionModel.connection_name)",
    )

    def __init__(self, name):
        self.profile_name = name

    def __repr__(self):
        return json.dumps(
            {"profile_id": self.profile_id, "profile_name": self.profile_name}
        )


class DeviceModel(Base):
    __tablename__ = "device"
    device_id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String(50), nullable=False)
    active_profile_id = Column(
        Integer, ForeignKey("profile.profile_id"), nullable=False
    )
    backref = backref("belongs_to_device", uselist=False)
    active_profile = relationship(ProfileModel, backref=backref, uselist=False)
    interfaces = relationship(
        "InterfaceModel",
        backref=backref,
        lazy=False,
        cascade="delete",
        order_by="asc(InterfaceModel.interface_id)",
    )

    def __init__(self, device_name, profile_id):
        self.device_name = device_name
        self.active_profile_id = profile_id

    def __repr__(self):
        return json.dumps(
            {
                "device_id": self.device_id,
                "device_name": self.device_name,
                "active_profile_id": self.active_profile_id,
            }
        )

    def serialize(self):
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "active_profile_name": self.active_profile.profile_name,
        }


class ManagementInterfaceModel(Base):
    __tablename__ = "management_interface"
    management_interface_id = Column(Integer, primary_key=True, autoincrement=True)
    interface_name = Column(String(20), nullable=False, unique=True)

    def __init__(self, interface_name):
        self.interface_name = interface_name

    def __repr__(self):
        return json.dumps(
            {
                "management_interface_id": self.management_interface_id,
                "interface_name": self.interface_name,
            }
        )


class LogicalInterfaceModel(Base):
    __tablename__ = "logical_interface"
    logical_interface_id = Column(Integer, primary_key=True, autoincrement=True)
    logical_name = Column(String(50), nullable=False, unique=True)

    def __init__(self, logical_name):
        self.logical_name = logical_name

    def __repr__(self):
        return json.dumps(
            {
                "logical_interface_id": self.logical_interface_id,
                "logical_name": self.logical_name,
            }
        )


class InterfaceModel(Base):
    __tablename__ = "interface"
    interface_id = Column(Integer, primary_key=True, autoincrement=True)
    physical_name = Column(String(50), nullable=False, unique=True)
    belongs_to_device_id = Column(
        Integer, ForeignKey("device.device_id"), nullable=False
    )
    has_logical_interface_id = Column(
        Integer,
        ForeignKey("logical_interface.logical_interface_id"),
        nullable=True,
    )
    backref = backref("physical_interfaces")
    has_logical_interface = relationship(
        LogicalInterfaceModel, backref=backref, uselist=False
    )
    interface_status = Column(
        Enum("up", "down", name="interface_status_enum"),
        nullable=False,
        default="up",
    )

    def __init__(self, physical_name, device_id, has_logical_interface_id=None):
        self.physical_name = physical_name
        self.belongs_to_device_id = device_id
        self.has_logical_interface_id = has_logical_interface_id

    def __repr__(self):
        if self.has_logical_interface_id is not None:
            return json.dumps(
                {
                    "interface_id": self.interface_id,
                    "physical_name": self.physical_name,
                    "has_logical_interface_id": self.has_logical_interface_id,
                    "belongs_to_device_id": self.belongs_to_device_id,
                    "status": self.interface_status,
                }
            )
        else:
            return json.dumps(
                {
                    "interface_id": self.interface_id,
                    "physical_name": self.physical_name,
                    "has_logical_interface_id": None,
                    "belongs_to_device_id": self.belongs_to_device_id,
                    "status": self.interface_status,
                }
            )

    def serialize(self):
        if self.has_logical_interface_id is not None:
            return {
                "interface_id": self.interface_id,
                "logical_name": self.has_logical_interface.logical_name,
                "physical_name": self.physical_name,
            }
        return {
            "interface_id": self.interface_id,
            "logical_name": "None",
            "physical_name": self.physical_name,
        }


class ConnectionModel(Base):
    __tablename__ = "connection"
    connection_id = Column(Integer, primary_key=True, autoincrement=True)
    connection_name = Column(String(50), nullable=False, unique=True)
    first_logical_interface_id = Column(
        Integer,
        ForeignKey("logical_interface.logical_interface_id"),
        nullable=False,
        unique=True,
    )
    first_logical_interface = relationship(
        LogicalInterfaceModel,
        lazy=False,
        foreign_keys=[first_logical_interface_id],
        uselist=False,
    )
    second_logical_interface_id = Column(
        Integer,
        ForeignKey("logical_interface.logical_interface_id"),
        nullable=False,
        unique=True,
    )
    second_logical_interface = relationship(
        LogicalInterfaceModel,
        lazy=False,
        foreign_keys=[second_logical_interface_id],
        uselist=False,
    )
    belongs_to_profile_id = Column(
        Integer, ForeignKey("profile.profile_id"), nullable=False
    )
    parameters = relationship(
        "ParameterModel",
        backref="belongs_to_connection",
        lazy=False,
        cascade="delete",
        order_by="asc(ParameterModel.parameter_name)",
    )

    def __init__(
        self,
        connection_name,
        first_logical_interface_id,
        second_logical_interface_id,
        profile_id,
    ):
        self.connection_name = connection_name
        self.first_logical_interface_id = first_logical_interface_id
        self.second_logical_interface_id = second_logical_interface_id
        self.belongs_to_profile_id = profile_id

    def __repr__(self):
        return json.dumps(
            {
                "connection_id": self.connection_id,
                "connection_name": self.connection_name,
                "first_logical_interface_id": self.first_logical_interface_id,
                "first_logical_interface_name": self.first_logical_interface.logical_name,
                "second_logical_interface_id": self.second_logical_interface_id,
                "second_logical_interface_name": self.second_logical_interface.logical_name,
                "belongs_to_profile_id": self.belongs_to_profile_id,
            }
        )

    def serialize(self):
        delay = DEFAULT_PARAMETERS[DELAY]
        packet_loss = DEFAULT_PARAMETERS[PACKET_LOSS]
        bandwidth = DEFAULT_PARAMETERS[BANDWIDTH]
        jitter = DEFAULT_PARAMETERS[JITTER]

        for parameter in self.parameters:
            if parameter.parameter_name == DELAY:
                delay = parameter.value

            if parameter.parameter_name == PACKET_LOSS:
                packet_loss = parameter.value

            if parameter.parameter_name == BANDWIDTH:
                bandwidth = parameter.value

            if parameter.parameter_name == JITTER:
                jitter = parameter.value

        return {
            "connection_name": self.connection_name,
            "interface1": self.first_logical_interface.logical_name,
            "interface2": self.second_logical_interface.logical_name,
            DELAY: delay,
            PACKET_LOSS: packet_loss,
            BANDWIDTH: bandwidth,
            JITTER: jitter,
        }


class ParameterModel(Base):
    __tablename__ = "parameter"
    parameter_id = Column(Integer, primary_key=True, autoincrement=True)
    parameter_name = Column(
        Enum(
            BANDWIDTH,
            DELAY,
            PACKET_LOSS,
            JITTER,
            name="parameter_name_enum",
        ),
        nullable=False,
    )
    value = Column(Integer, nullable=False)
    direction = Column(
        Enum(
            INCOMING,
            OUTGOING,
            name="direction_enum",
        ),
        nullable=False,
    )
    belongs_to_connection_id = Column(
        Integer, ForeignKey("connection.connection_id"), nullable=False
    )

    def __init__(self, parameter_name, value, direction, connection_id):
        self.parameter_name = parameter_name
        self.value = value
        self.direction = direction
        self.belongs_to_connection_id = connection_id

    def __repr__(self):
        return json.dumps(
            {
                "parameter_id": self.parameter_id,
                "parameter_name": self.parameter_name,
                "value": self.value,
                "direction": self.direction,
                "connection_id": self.belongs_to_connection_id,
            }
        )


Base.metadata.create_all(database_engine)
