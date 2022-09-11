import logging
import subprocess


class CommandError(Exception):
    def __init__(self, cmd: str, return_code: int) -> None:
        self.cmd = cmd
        self.return_code = return_code


def cmd_run(*cmd) -> str:
    """Run command with subprocess

    Args:
        cmd: The command to run

    Returns:
        The output from the command

    Raises:
        CommandError when command return code isn't  0
    """

    logging.debug(f"Run command: '{cmd}'")
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if process.returncode != 0:
        raise CommandError(cmd="".join(cmd), return_code=process.returncode)
    return process.stdout
