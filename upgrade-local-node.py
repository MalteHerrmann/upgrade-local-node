#!/usr/bin/python3
"""
upgrade-local-node.py | Malte Herrmann

This script executes the necessary commands to upgrade a local node to a given 
target version.
"""

import os
import re
import subprocess
import sys
import time


EVMOSD_HOME = os.path.join(os.path.expanduser("~"), ".tmp-evmosd")
DEFAULT_FLAGS = "--home ~/.tmp-evmosd --chain-id evmos_9000-1 --keyring-backend test --gas auto --fees 100000000000000000aevmos --gas-adjustment 1.3 -b block -y"


def build_upgrade_proposal(target_version: str, upgrade_height: int) -> str:
    """
    Builds the command string to submit a software upgrade proposal.
    """
    command = f"evmosd tx gov submit-legacy-proposal software-upgrade {target_version}"
    title = f"--title 'Upgrade to {target_version}'"
    description = f"--description 'Upgrade to {target_version}'"
    upgrade_height = f"--upgrade-height {upgrade_height}"
    deposit = "--deposit 100000000000000000000aevmos"

    return f"{command} {title} {description} {upgrade_height} {deposit} --no-validate"


def execute_shell_command(command: str, home: str=EVMOSD_HOME, sender: str="dev0", defaults: bool=True) -> str:
    """
    Runs a subprocess to execute the given shell command.
    """
    home_flag = f" --home {home}"
    sender_flag = f" --from {sender}"
    full_command = command + home_flag + sender_flag
    if defaults:
        full_command += " " + DEFAULT_FLAGS

    try:
        output = subprocess.check_output(full_command, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

    parse_output(output)

    return output.strip()


def parse_output(output: str):
    """
    Parses the output of a shell command.
    """
    print(output)


def upgrade_local_node(target_version: str):
    """
    Upgrades a local running instance of an Evmos node using a governance proposal.
    """
    upgrade_proposal = build_upgrade_proposal(target_version, 25)
    execute_shell_command(upgrade_proposal)
    wait(2)
    execute_shell_command("evmosd tx gov vote 1 yes")
    wait(2)
    execute_shell_command("evmosd tx gov vote 1 yes", sender="dev1")
    wait(2)
    execute_shell_command("evmosd tx gov vote 1 yes", sender="dev2")


def wait(seconds: int):
    """
    Waits for a given number of seconds.
    """
    time.sleep(seconds)


if __name__=='__main__':
    target_version = sys.argv[1]
    if not re.search("v\d+\.\d\.\d", target_version):
        print("Invalid target version. Please use the format vX.Y.Z(-rc*).")
        sys.exit(2)

    upgrade_local_node(target_version)
