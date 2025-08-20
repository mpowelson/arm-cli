import os
import subprocess


def _validate_cmd(cmd):
    """
    Ensure command is a list of strings, no shell=True, no None elements.
    """
    if not isinstance(cmd, list):
        raise ValueError("Command must be a list of arguments")
    if any(not isinstance(c, str) for c in cmd):
        raise ValueError("All command arguments must be strings")
    # Optionally sanitize paths or arguments further here if needed


def safe_run(cmd, **kwargs):
    """
    Safe subprocess.run wrapper.
    - cmd must be a list
    - shell=True is prohibited
    - check, capture_output, etc. passed through
    """
    _validate_cmd(cmd)
    if kwargs.get("shell", False):
        raise ValueError("shell=True not allowed for security reasons")
    return subprocess.run(cmd, **kwargs)  # nosec B603


def sudo_run(cmd, **kwargs):
    """
    Safe subprocess.run wrapper that runs command with sudo.
    - Prepends 'sudo' to cmd
    - Performs same safety checks
    """
    _validate_cmd(cmd)
    if kwargs.get("shell", False):
        raise ValueError("shell=True not allowed for security reasons")
    full_cmd = ["sudo"] + cmd
    return subprocess.run(full_cmd, **kwargs)  # nosec B603
