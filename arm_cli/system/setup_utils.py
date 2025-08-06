import os
import stat
import subprocess
import sys

from arm_cli.system.shell_scripts import detect_shell, get_current_shell_addins


def check_xhost_setup():
    """Check if xhost is already configured for Docker"""
    try:
        result = subprocess.run(["xhost"], capture_output=True, text=True, check=True)
        return "LOCAL:docker" in result.stdout
    except subprocess.CalledProcessError:
        return False


def setup_xhost(force=False):
    """Setup xhost for GUI applications"""
    try:
        # Check if xhost is already configured
        if check_xhost_setup():
            print("X11 access for Docker containers is already configured.")
            return

        # Ensure xhost allows local Docker connections
        print("Setting up X11 access for Docker containers...")
        if not force:
            response = (
                input("Do you want to configure X11 access for Docker containers? (y/N): ")
                .strip()
                .lower()
            )
            if response not in ["y", "yes"]:
                print("X11 setup cancelled.")
                return

        subprocess.run(["xhost", "+local:docker"], check=True)
        print("xhost configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring xhost: {e}")


def check_sudo_privileges():
    """Check if the user has sudo privileges"""
    try:
        subprocess.run(["sudo", "-n", "true"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def check_data_directories_setup():
    """Check if data directories are already properly set up"""
    data_dirs = ["/DATA/influxdb2", "/DATA/images", "/DATA/node_exporter"]
    current_uid = os.getuid()
    current_gid = os.getgid()

    for directory in data_dirs:
        # Check if directory exists
        if not os.path.exists(directory):
            return False

        # Check ownership
        try:
            stat_info = os.stat(directory)
            if stat_info.st_uid != current_uid or stat_info.st_gid != current_gid:
                return False

            # Check permissions (should be 775)
            mode = stat_info.st_mode
            if not (mode & stat.S_IRWXU and mode & stat.S_IRWXG and not mode & stat.S_IWOTH):
                return False

        except (OSError, PermissionError):
            return False

    return True


def setup_data_directories(force=False):
    """Setup data directories for the ARM system"""
    try:
        # Check if directories are already properly set up
        if check_data_directories_setup():
            print("Data directories are already properly set up.")
            return True

        print("Setting up data directories...")

        # Check if user has sudo privileges
        if not check_sudo_privileges():
            print("This operation requires sudo privileges.")
            print("Please run: sudo arm-cli system setup")
            return False

        # Ask user for confirmation
        print("This will create the following directories:")
        data_dirs = ["/DATA/influxdb2", "/DATA/images", "/DATA/node_exporter"]
        for directory in data_dirs:
            print(f"  - {directory}")
        print("And set appropriate ownership and permissions.")

        if not force:
            response = input("Do you want to proceed? (y/N): ").strip().lower()
            if response not in ["y", "yes"]:
                print("Setup cancelled.")
                return False

        # Get current user UID and GID
        uid = os.getuid()
        gid = os.getgid()

        print("Creating directories and setting permissions...")

        # Create all directories in one sudo command
        mkdir_cmd = ["sudo", "mkdir", "-p"] + data_dirs
        subprocess.run(mkdir_cmd, check=True)
        print("Created directories.")

        # Set ownership for all directories in one sudo command
        chown_cmd = ["sudo", "chown", "-R", f"{uid}:{gid}"] + data_dirs
        subprocess.run(chown_cmd, check=True)
        print("Set ownership.")

        # Set permissions for all directories in one sudo command
        chmod_cmd = ["sudo", "chmod", "-R", "775"] + data_dirs
        subprocess.run(chmod_cmd, check=True)
        print("Set permissions.")

        print("Data directories setup completed successfully.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error setting up data directories: {e}")
        print("Please ensure you have sudo privileges.")
        return False
    except Exception as e:
        print(f"Unexpected error during data directory setup: {e}")
        return False


def is_line_in_file(line, filepath) -> bool:
    """Checks if a line is already in a file"""
    with open(filepath, "r") as f:
        return any(line.strip() in l.strip() for l in f)


def setup_shell(force=False):
    """Setup shell addins for autocomplete"""
    shell = detect_shell()

    if "bash" in shell:
        bashrc_path = os.path.expanduser("~/.bashrc")
        line = f"source {get_current_shell_addins()}"
        if not is_line_in_file(line, bashrc_path):
            print(f'Adding \n"{line}"\nto {bashrc_path}')
            if not force:
                response = (
                    input("Do you want to add shell autocomplete to ~/.bashrc? (y/N): ")
                    .strip()
                    .lower()
                )
                if response not in ["y", "yes"]:
                    print("Shell setup cancelled.")
                    return

            with open(bashrc_path, "a") as f:
                f.write(f"\n{line}\n")
        else:
            print("Shell addins are already configured in ~/.bashrc")
    else:
        print(f"Unsupported shell: {shell}", file=sys.stderr)
