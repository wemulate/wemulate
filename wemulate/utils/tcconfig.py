import os
import shutil
from typing import Dict, List, Tuple
from cement.core import interface
from pyroute2 import IPRoute
from cement import shell
from wemulate.core.exc import WEmulateExecutionError, WEmulateFileError

CONFIG_PATH: str = "/etc/wemulate/config"
BRIDGE_CONFIG_FILE: str = "bridge.conf"
TC_CONFIG_FILE: str = "tc.conf"
ip: IPRoute = IPRoute()


def _execute_in_shell(command: str) -> None:
    try:
        stdout, stderr, exitcode = shell.cmd(command)
        if stderr and exitcode != 0:
            raise WEmulateExecutionError(
                f"stdout: {stdout} | stderr: {stderr} | exitcode: {exitcode}"
            )
    except WEmulateExecutionError as e:
        raise e
    except Exception as e:
        raise WEmulateExecutionError


def _execute_commands(commands: List[str]) -> None:
    for command in commands:
        _execute_in_shell(command)


def _add_delay_command(delay_value) -> str:
    return f" --delay {delay_value}ms"


def _add_jitter_command(mean_delay, jitter_value) -> str:
    return f" --delay {mean_delay}ms --delay-distro {jitter_value}ms"


def _add_packet_loss_command(packet_loss_value) -> str:
    return f" --loss {packet_loss_value}%"


def _add_bandwidth_incoming_command(bandwidth_value) -> str:
    return f" --direction incoming --rate {bandwidth_value}Mbps"


def _add_bandwidth_outgoing_command(bandwidth_value) -> str:
    return f" --direction outgoing --rate {bandwidth_value}Mbps"


def _add_duplication_command(duplication_value) -> str:
    return f" --duplicate {duplication_value}%"


def _add_corruption_command(corruption_value) -> str:
    return f" --corrupt {corruption_value}%"


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


def set_parameters(
    connection_name: str, interface_name: str, parameters: Dict[str, int]
) -> None:
    """
    Sets the given parameters on the specified interface.

    Args:
        interface_name: This is the name of the interface which should be configured.
        parameters: This is a dict of parameters which should be applied {parameter_name: parameter_value}.

    Returns:
        None

    Raises:
        WEmulateExecutionError: if the parameters could not be applied to the interface
    """
    outgoing_config_command: str = f"tcset {interface_name} "
    commands_to_execute: List[str] = []
    mean_delay = 0.001  # smallest possible delay
    if parameters:
        remove_parameters(connection_name, interface_name)
        if "delay" in parameters:
            mean_delay = parameters["delay"]
            if "jitter" not in parameters:
                outgoing_config_command += _add_delay_command(mean_delay)
        if "jitter" in parameters:
            outgoing_config_command += _add_jitter_command(
                mean_delay, 2 * int(parameters["jitter"])
            )
        if "packet_loss" in parameters:
            outgoing_config_command += _add_packet_loss_command(
                parameters["packet_loss"]
            )
        if "duplication" in parameters:
            outgoing_config_command += _add_duplication_command(
                parameters["duplication"]
            )
        if "corruption" in parameters:
            outgoing_config_command += _add_corruption_command(parameters["corruption"])
        if "bandwidth" in parameters:
            outgoing_config_command += _add_bandwidth_outgoing_command(
                parameters["bandwidth"]
            )
            incoming_config_command: str = f"tcset {interface_name} "
            incoming_config_command += _add_bandwidth_incoming_command(
                parameters["bandwidth"]
            )
            incoming_config_command += " --change"
            commands_to_execute.append(incoming_config_command)
        outgoing_config_command += " --change"
        commands_to_execute.append(outgoing_config_command)
        _execute_commands(commands_to_execute)
        _write_commands_to_tc_config_file(connection_name, commands_to_execute)


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
    # Here we have to delete the whole input in the tc.conf file -> we need the connection_name
