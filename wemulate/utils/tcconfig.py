import os
import shutil
import subprocess
from typing import Dict, List, Optional

from pyroute2 import IPRoute

from wemulate.core.database.models import (
    CORRUPTION,
    DUPLICATION,
    INCOMING,
    OUTGOING,
    DELAY,
    PACKET_LOSS,
    BANDWIDTH,
    JITTER,
)
from wemulate.core.exc import WEmulateExecutionError, WEmulateFileError


CONFIG_PATH: str = "/var/lib/wemulate/config"
BRIDGE_CONFIG_FILE: str = "bridge.conf"
TC_CONFIG_FILE: str = "tc.conf"
ip: IPRoute = IPRoute()
SMALLEST_POSSIBLE_DELAY: int = 1


def _execute_in_shell(command: str) -> None:
    try:
        completed_process = subprocess.run(command.split(), capture_output=True)
        if completed_process.stderr and completed_process.returncode != 0:
            raise WEmulateExecutionError(
                f"stdout: {completed_process.stdout} | stderr: {completed_process.stderr} | exitcode: {completed_process.returncode}"
            )
    except WEmulateExecutionError as e:
        raise e
    except Exception as e:
        raise WEmulateExecutionError


def _execute_commands(commands: List[str]) -> None:
    for command in commands:
        _execute_in_shell(command)


def _add_delay_command(
    parameters: Dict[str, Dict[str, int]], mean_delay: int, direction: str
) -> str:
    if DELAY in parameters[direction]:
        if JITTER not in parameters[direction]:
            return f" --delay {mean_delay}ms"
    return ""


def _add_jitter_command(
    parameters: Dict[str, Dict[str, int]], mean_delay: int, direction: str
) -> str:
    return (
        f" --delay {mean_delay}ms --delay-distro {parameters[direction][JITTER]}ms"
        if JITTER in parameters[direction]
        else ""
    )


def _add_packet_loss_command(
    parameters: Dict[str, Dict[str, int]], direction: str
) -> str:
    return (
        f" --loss {parameters[direction][PACKET_LOSS]}%"
        if PACKET_LOSS in parameters[direction]
        else ""
    )


def _add_bandwidth_command(
    parameters: Dict[str, Dict[str, int]], direction: str
) -> str:
    return (
        f" --rate {parameters[direction][BANDWIDTH]}Mbps"
        if BANDWIDTH in parameters[direction]
        else ""
    )


def _add_duplication_command(
    parameters: Dict[str, Dict[str, int]], direction: str
) -> str:
    return (
        f" --duplicate {parameters[direction][DUPLICATION]}%"
        if DUPLICATION in parameters[direction]
        else ""
    )


def _add_corruption_command(
    parameters: Dict[str, Dict[str, int]], direction: str
) -> str:
    return (
        f" --corrupt {parameters[direction][CORRUPTION]}%"
        if CORRUPTION in parameters[direction]
        else ""
    )


def _add_config_files_if_not_exist(connection_name: str) -> None:
    connection_config_path: str = f"{CONFIG_PATH}/{connection_name}/"
    if not os.path.exists(connection_config_path):
        os.makedirs(connection_config_path)


def _delete_config_files(connection_name: str) -> None:
    connection_config_path: str = f"{CONFIG_PATH}/{connection_name}/"
    if os.path.exists(connection_config_path):
        shutil.rmtree(connection_config_path, ignore_errors=True)


def _write_commands_into_config_file(
    connection_name: str, config_file_name: str, write_mode: str, commands: List[str]
) -> None:
    config_file_path: str = f"{CONFIG_PATH}/{connection_name}/{config_file_name}"
    with open(config_file_path, write_mode) as config_file:
        for command in commands:
            config_file.write(f"{command}\n")


def _write_commands_to_bridge_config_file(
    connection_name: str, commands: List[str]
) -> None:
    _write_commands_into_config_file(connection_name, BRIDGE_CONFIG_FILE, "a", commands)


def _write_commands_to_tc_config_file(
    connection_name: str, commands: List[str]
) -> None:
    _write_commands_into_config_file(connection_name, TC_CONFIG_FILE, "w", commands)


def _add_and_activate_linux_bridge(connection_name: str) -> None:
    commands: List[str] = [
        f"ip link add name {connection_name} type bridge",
        f"ip link set dev {connection_name} up",
    ]
    _execute_commands(commands)
    _write_commands_to_bridge_config_file(connection_name, commands)


def _add_interfaces_to_bridge(
    connection_name: str, interface1_name: str, interface2_name: str
) -> None:
    commands: List[str] = [
        f"ip link set dev {interface} master {connection_name}"
        for interface in (interface1_name, interface2_name)
    ]
    _execute_commands(commands)
    _write_commands_to_bridge_config_file(connection_name, commands)


def _delete_linux_bridge(connection_name: str) -> None:
    _execute_in_shell(f"ip link del {connection_name}")


def add_connection(
    connection_name: str, interface1_name: str, interface2_name: str
) -> None:
    """
    Adds a new logical connection in the WEmulate context and creates a linux bridge on the host system.

    Args:
        connection_name: This is the name of the connection which should be configured.
        interface1_name: This is the first interface which should be added to the connection/bridge.
        interface2_name: This is the second interface which should be added to the connection/bridge.

    Returns:
        None

    Raises:
        WEmulateExecutionError: if the bridge could not be added successfully
        WEmulateFileError: if the configuration files could not be created or modified
    """
    try:
        _add_config_files_if_not_exist(connection_name)
        _add_and_activate_linux_bridge(connection_name)
        _add_interfaces_to_bridge(connection_name, interface1_name, interface2_name)
    except OSError as e:
        raise WEmulateFileError(message=f"Error: {e.strerror} | Filename: {e.filename}")


def remove_connection(connection_name: str) -> None:
    """
    Removes the specified connection and deletes the linux bridge on the host system.

    Args:
        connection_name: This is the name of the connection which should be removed.

    Returns:
        None

    Raises:
        WEmulateExecutionError: if the bridge could not be removed successfully
        WEmulateFileError: if the connection configuration file could not be removed successfully
    """
    try:
        _delete_linux_bridge(connection_name)
        _delete_config_files(connection_name)
    except OSError as e:
        raise WEmulateFileError(message=f"Error: {e.strerror} | Filename: {e.filename}")


def _create_base_command(interface_name: str, direction: Optional[str]) -> str:
    return f"tcset {interface_name} --direction {direction}"


def _create_config_command(
    parameters: Dict[str, Dict[str, int]],
    interface_name: str,
    direction: str,
    mean_delay: int,
) -> str:
    base_command: str = _create_base_command(interface_name, direction)
    base_command += _add_delay_command(parameters, mean_delay, direction)
    base_command += _add_jitter_command(parameters, mean_delay, direction)
    base_command += _add_packet_loss_command(parameters, direction)
    base_command += _add_bandwidth_command(parameters, direction)
    base_command += _add_duplication_command(parameters, direction)
    base_command += _add_corruption_command(parameters, direction)
    return base_command


def set_parameters(
    connection_name: str,
    interface_name: str,
    parameters: Dict[str, Dict[str, int]],
    direction: Optional[str],
) -> None:
    """
    Sets the given parameters on the specified interface.

    Args:
        connection_name: This is the name of the connection which is involved
        interface_name: This is the name of the interface which should be configured.
        parameters: This is a dict of parameters which should be applied {parameter_name: parameter_value}.

    Returns:
        None

    Raises:
        WEmulateExecutionError: if the parameters could not be applied to the interface
    """
    remove_parameters(connection_name, interface_name)
    for direction in [INCOMING, OUTGOING]:
        if parameters[direction]:
            mean_delay = (
                parameters[direction][DELAY]
                if DELAY in parameters[direction]
                else SMALLEST_POSSIBLE_DELAY
            )
            config_command: str = _create_config_command(
                parameters, interface_name, direction, mean_delay
            )
            _execute_in_shell(config_command)
            _write_commands_to_tc_config_file(connection_name, [config_command])


def remove_parameters(connection_name: str, interface_name: str) -> None:
    """
    Deletes all configured parameters on the given interface.

    Args:
        interface_name: This is the name of the interface on which the parameters should be removed.

    Returns:
        None

    Raises:
        WEmulateExecutionError: if the parameters could not be removed from the interface
    """
    _execute_in_shell(f"tcdel {interface_name} --all")
    _write_commands_to_tc_config_file(connection_name, [""])
