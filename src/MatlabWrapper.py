import logging
import os
import subprocess
from shutil import which
import sys

logger = logging.getLogger(__name__)

"""
Make it easy to execute the MATLAB CLI from Python, and 
do so from both a regular linux terminal and from a CI 
environment (e.g., GitHub Actions) where the MATLAB 
license is provided via a token.

Assumes that the MATLAB CLI is installed and available in the PATH, and
code lives at         
   default_matlab_path = "/app"
   local_matlab_path = "src"

"""

default_matlab_path = "/app"
local_matlab_path = "src"
PATHS_TO_ADD = [default_matlab_path, local_matlab_path]


def setup_matlab_path(paths: list[str], matlab_command):
    add_path_commands = ""
    for path in paths if isinstance(paths, list) else [paths]:
        add_path_commands += f'addpath(genpath("{path}")); '
    cmd = [matlab_command, "-nodesktop", "-batch", f"'{add_path_commands} savepath;'"]

    logger.info(f"MATLAB setup command: \n  {' '.join(cmd)}")

    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    while (line := p.stdout.readline()) != "":  # type: ignore
        line = line.rstrip()
        logger.info(line)

    p.wait(timeout=60)
    if p.returncode != 0:
        logger.error(f"MATLAB setup command failed with return code {p.returncode}")
        raise RuntimeError(
            f"MATLAB setup command failed with return code {p.returncode}"
        )


def get_matlab_command():
    """
    Returns the appropriate MATLAB command based on the environment.
    If running in a CI environment with a license token, it returns 'matlab-batch'.
    Otherwise, it returns 'matlab'.
    """
    if (
        os.getenv("CI") == "true"
        and os.getenv("MLM_LICENSE_TOKEN")
        and (which("matlab-batch") is not None)
    ):
        return "matlab-batch"
    else:
        return "matlab"


def call_matlab(command, init_paths=True, timeout=60 * 5):
    MATLAB_COMMAND = get_matlab_command()
    if init_paths:
        
        setup_matlab_path(PATHS_TO_ADD, MATLAB_COMMAND)
        logger.info(
            f"Added {local_matlab_path} and {default_matlab_path} files to path"
        )

    cmd = [MATLAB_COMMAND, "-nodesktop", "-batch"]
    cmd.append(command)

    logger.info(f"Calling MATLAB with command: \n  {' '.join(cmd)}")
    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    while (line := p.stdout.readline()) != "":  # type: ignore
        line = line.rstrip()
        logger.info(line)

    p.wait(timeout=timeout)

    logger.info(f"MATLAB process finished with return code {p.returncode}")

    if p.returncode != 0:
        logger.error(f"MATLAB command failed with return code {p.returncode}")
        raise RuntimeError(f"MATLAB command failed with return code {p.returncode}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # any args should be passed to the MATLAB command as a single string
    if len(sys.argv) > 1:
        matlab_command = " ".join(sys.argv[1:])
        call_matlab(matlab_command, init_paths=False)
    else:
        call_matlab("disp('Hello from MATLAB via python!')", init_paths=False)