#!/usr/bin/env bash

## Setup autocomplete for arm-cli
setup_arm_cli_completion() {
    if command -v arm-cli >/dev/null 2>&1; then
        local completion_script="$HOME/.arm_cli_completion.sh"
        # Generate completion script if it doesn't exist or arm-cli was updated
        if [ ! -f "$completion_script" ] || [ "$(command -v arm-cli)" -nt "$completion_script" ]; then
            _ARM_CLI_COMPLETE=bash_source arm-cli > "$completion_script" 2>/dev/null
        fi

        # Source the script or fallback to dynamic completion
        if [ -f "$completion_script" ]; then
            source "$completion_script"
        else
            eval "$(_ARM_CLI_COMPLETE=bash_source arm-cli)"
        fi
    fi
}

## Setup alias and completion
setup_alias() {
    local alias_name="aa"
    local cli_path
    cli_path=$(command -v arm-cli)

    if [ -n "$cli_path" ]; then
        if [[ $- == *i* ]]; then  # Only define alias in interactive shells
            alias "$alias_name"="$cli_path"
            complete -o default -F _arm_cli_completion "$alias_name" 2>/dev/null || true
        fi
    fi
}

## Set UID for Docker
export CURRENT_UID="$(id -u):$(id -g)"

## Allow Docker containers to access X11
allow_x11_docker_access() {
    if command -v xhost >/dev/null 2>&1; then
        xhost +local:docker >/dev/null 2>&1
    fi
}

## Add user to docker group if needed
ensure_docker_group() {
    if ! id -nG "$USER" | grep -qw docker; then
        echo "Adding $USER to docker group..."
        sudo usermod -aG docker "$USER"
        echo "Please log out and back in for the docker group changes to take effect,"
        echo "or run 'newgrp docker' in a new terminal session."
    else
        # User is already in group; try to activate it
        newgrp docker >/dev/null 2>&1 || true
    fi
}

# Run setup steps
setup_arm_cli_completion
setup_alias
allow_x11_docker_access
ensure_docker_group
