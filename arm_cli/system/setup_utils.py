import os
import subprocess
import sys

from arm_cli.system.shell_scripts import get_current_shell_addins, detect_shell

def setup_xhost():
    """Setup xhost for GUI applications"""
    try:
        # Ensure xhost allows local Docker connections
        print("Setting up X11 access for Docker containers...")
        subprocess.run(["xhost", "+local:docker"], check=True)
        print("xhost configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring xhost: {e}")


def is_line_in_file(line, filepath) -> bool:
    """Checks if a line is already in a file"""
    with open(filepath, "r") as f:
        return any(line.strip() in l.strip() for l in f)

def setup_shell():
    """Setup shell addins for autocomplete"""
    shell = detect_shell()

    if "bash" in shell:
        bashrc_path = os.path.expanduser("~/.bashrc")
        line = f"source {get_current_shell_addins()}"
        if not is_line_in_file(line, bashrc_path):
            print(f'Adding \n"{line}"\nto {bashrc_path}')
            with open(bashrc_path, "a") as f:
                f.write(f"\n{line}\n")
    else:
        print(f"Unsupported shell: {shell}", file=sys.stderr)
                

