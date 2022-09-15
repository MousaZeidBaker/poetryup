import logging
import subprocess
from typing import List


class CommandError(Exception):
    def __init__(self, cmd: str, return_code: int) -> None:
        self.cmd = cmd
        self.return_code = return_code


def cmd_run(cmd: List, capture_output: bool = False) -> str:
    """Run command with subprocess

    Args:
        cmd: The command to run
        capture_output: Capture process output

    Returns:
        The output from the command

    Raises:
        CommandError when command exists with non-zero exit code
    """

    logging.debug(f"Run command: '{' '.join(cmd)}'")
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.STDOUT if capture_output else None,
    )
    if process.returncode != 0:
        logging.debug(
            f"Command '{' '.join(cmd)}' exited with non-zero"
            f"exit code '{process.returncode}'"
        )
        raise CommandError(cmd="".join(cmd), return_code=process.returncode)
    return process.stdout.decode() if capture_output else None
