import os
from typing import List, Tuple
from pyroute2 import IPRoute
from cement import shell
from wemulate.core.exc import WEmulateExecutionError

BRIDGE_CONFIG_PATH = "/etc/network/interfaces.d"
ip = IPRoute()


def _execute_in_shell(command: str) -> None:
    try:
        # stdout, stderr, exitcode = shell.cmd(command)
        shell.cmd(command)
        # TODO implement exitcode strategy
        # raise Exception
    except:
        raise WEmulateExecutionError


def _execute_commands(command_tuple: Tuple) -> None:
    outgoing_command, incomming_command = command_tuple
    _execute_in_shell(outgoing_command)
    _execute_in_shell(incomming_command)


def _add_delay_command(delay_value) -> str:
    return f"--delay {delay_value}ms"


def _add_jitter_command(mean_delay, jitter_value) -> str:
    return f"--delay {mean_delay}ms --delay-distro {jitter_value}ms"


def _add_packet_loss_command(packet_loss_value) -> str:
    return f"--loss {packet_loss_value}%"


def _add_bandwidth_incoming_command(bandwidth_value) -> str:
    return f"--direction incoming --rate {bandwidth_value}Mbps"


def _add_bandwidth_outgoing_command(bandwidth_value) -> str:
    return f"--direction outgoing --rate {bandwidth_value}Mbps"


def _add_duplication_command(duplication_value) -> str:
    return f"--duplicate {duplication_value}%"


def _add_corruption_command(corruption_value) -> str:
    return f"--corrupt {corruption_value}%"


def add_connection(
    connection_name: str, interface1_name: str, interface2_name: str
) -> None:
    """
    Adds a new connection.

    Args:
        connection_name: This is the name of the connection which should be configured.
        interface1_name: This is the first interface which should be added to the connection.
        inteface2_name: This is the second interface which should be added to the connection.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    INTERFACE_CONFIG_PATH = "/etc/network/interfaces"

    with open(INTERFACE_CONFIG_PATH, "r+") as interfaces_config_file:
        if BRIDGE_CONFIG_PATH not in interfaces_config_file.read():
            interfaces_config_file.write(f"source {BRIDGE_CONFIG_PATH}/*\n")

    connection_template = f"# Bridge Setup {connection_name}\nauto {connection_name}\niface {connection_name} inet manual\n    bridge_ports {interface1_name} {interface2_name}\n    bridge_stp off\n"

    if not os.path.exists("BRIDGE_CONFIG_PATH"):
        os.makedirs("BRIDGE_CONFIG_PATH")

    with open(f"{BRIDGE_CONFIG_PATH}/{connection_name}", "w") as connection_file:
        connection_file.write(connection_template)

    _execute_in_shell(
        f"sudo iptables -I WEMULATE -i {connection_name} -o {connection_name} -j ACCEPT"
    )

    return _execute_in_shell("sudo systemctl restart networking.service")


def remove_connection(connection_name: str) -> bool:
    """
    Removes the specified connection.

    Args:
        connection_name: This is the name of the connection which should be removed.

    Returns:
        True if the execution was successful. False when the execution failed.

    Raises:
        KeyError: Raises an exception.
    """
    ip.link("set", index=ip.link_lookup(ifname=connection_name)[0], state="down")
    _execute_in_shell(f"sudo brctl delbr {connection_name}")

    connection_file = f"{BRIDGE_CONFIG_PATH}/{connection_name}"
    if os.path.exists(connection_file):
        os.remove(connection_file)

    try:
        _execute_in_shell(
            f"sudo iptables -D WEMULATE -i {connection_name} -o {connection_name} -j ACCEPT"
        )
        return True
    except:
        return False


def set_parameters(interface_name, parameters):
    """
    Sets the given parameters on the specified interface.

    Args:
        interface_name: This is the name of the interface which should be configured.
        parameters: This is a list of parameters which should be applied.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    outgoing_config_command = f"sudo tcset {interface_name}"
    incoming_config_command = f"sudo tcset {interface_name}"
    mean_delay = 0.001  # smallest possible delay
    if parameters:
        if "delay" in parameters:
            mean_delay = parameters["delay"]
            if "jitter" not in parameters:
                outgoing_config_command += _add_delay_command(mean_delay)
        if "jitter" in parameters:
            outgoing_config_command += _add_jitter_command(
                mean_delay, 2 * parameters["jitter"]
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
            incoming_config_command += _add_bandwidth_incoming_command(
                parameters["bandwidth"]
            )
        command_tuple = (outgoing_config_command, incoming_config_command)
        return _execute_commands(command_tuple)
    return "No parameters were given!"


def remove_parameters(interface_name: str):
    """
    Deletes all configured parameters on the given interface.

    Args:
        interface_name: This is the name of the interface which should be configured.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    command = f"sudo tcdel {interface_name} --all"
    return _execute_in_shell(command)