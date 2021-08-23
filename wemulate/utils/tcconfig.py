import os
from typing import Dict, List, Tuple
from cement.core import interface
from pyroute2 import IPRoute
from cement import shell
from wemulate.core.exc import WEmulateExecutionError, WEmulateFileError

CONFIG_PATH: str = "/etc/wemulate/config/"
ip: IPRoute = IPRoute()


def _execute_in_shell(command: str) -> None:
    try:
        stdout, stderr, exitcode = shell.cmd(command)
        if stderr:
            raise WEmulateExecutionError(
                f"stdout: {stdout} | stderr: {stderr} | exitcode: {exitcode}"
            )
    except WEmulateExecutionError as e:
        raise e
    except Exception as e:
        raise WEmulateExecutionError


def _execute_commands(commands: List[str]) -> None:
    for command in commands:
        print(command)
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


def _add_config_folder_if_not_exist() -> None:
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)


def _add_and_activate_linux_bridge(connection_name: str) -> None:
    _execute_in_shell(f"ip link add name {connection_name} type bridge")
    _execute_in_shell(f"ip link set dev {connection_name} up")


def _add_interfaces_to_bridge(
    connection_name: str, interface1_name: str, interface2_name: str
) -> None:
    for interface in (interface1_name, interface2_name):
        _execute_in_shell(f"ip link set dev {interface} master {connection_name}")


def _add_linux_bridge(
    connection_name: str, interface1_name: str, interface2_name: str
) -> None:
    try:
        _add_config_folder_if_not_exist()
        _add_and_activate_linux_bridge(connection_name)
        _add_interfaces_to_bridge(connection_name, interface1_name, interface2_name)
    except OSError as e:
        raise WEmulateFileError(message=f"Error: {e.strerror} | Filename: {e.filename}")


def _add_iptables_rule(connection_name: str) -> None:
    _execute_in_shell(
        f"sudo iptables -I FORWARD -i {connection_name} -o {connection_name} -j ACCEPT"
    )


def _restart_network_service() -> None:
    _execute_in_shell("sudo systemctl restart networking.service")


def _delete_linux_bridge(connection_name: str) -> None:
    _execute_in_shell(f"ip link del {connection_name}")


def _remove_iptables_rule(connection_name: str) -> None:
    _execute_in_shell(
        f"sudo iptables -D WEMULATE -i {connection_name} -o {connection_name} -j ACCEPT"
    )


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
    _add_linux_bridge(connection_name, interface1_name, interface2_name)
    # _add_iptables_rule(connection_name)
    # _restart_network_service()


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
    _delete_linux_bridge(connection_name)
    # _remove_iptables_rule(connection_name)


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


def remove_parameters(interface_name: str) -> None:
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
