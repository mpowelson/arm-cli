"""Generate static bash completion from CLI structure"""

import click

# Default aliases for arm-cli
DEFAULT_ALIASES = ["arm-cli"]


def generate_completion_script(aliases: list[str] | None = None):
    """Generate static bash completion by introspecting the CLI

    Args:
        aliases: List of command names to enable completion for.
                 Defaults to ["arm-cli"]. Examples: ["arm-cli", "arm", "aa"]
    """
    from arm_cli.cli import cli

    if aliases is None:
        aliases = DEFAULT_ALIASES

    # Collect commands and flags at each level
    commands = {}
    flags = {}

    def collect_commands(group, prefix=""):
        """Recursively collect all commands and their flags"""
        if isinstance(group, click.Group):
            # For LazyGroup, we need to load commands
            if hasattr(group, "lazy_subcommands"):
                cmd_names = list(group.lazy_subcommands.keys())
            else:
                cmd_names = list(group.commands.keys())

            commands[prefix] = cmd_names

            # Collect flags for this group
            group_flags = ["-h", "--help"]  # Click always adds these
            if hasattr(group, "params"):
                for param in group.params:
                    if isinstance(param, click.Option):
                        group_flags.extend(param.opts)
            flags[prefix] = group_flags

            # Recursively collect subcommands
            for cmd_name in cmd_names:
                cmd = group.get_command(None, cmd_name)
                if cmd:
                    new_prefix = f"{prefix}.{cmd_name}" if prefix else cmd_name

                    # Collect flags for this command
                    cmd_flags = ["-h", "--help"]  # Click always adds these
                    if hasattr(cmd, "params"):
                        for param in cmd.params:
                            if isinstance(param, click.Option):
                                cmd_flags.extend(param.opts)
                    flags[new_prefix] = cmd_flags

                    if isinstance(cmd, click.Group):
                        collect_commands(cmd, new_prefix)

    # Start collection
    collect_commands(cli)

    # Generate bash script
    aliases_comment = ", ".join(aliases)
    script = f"""#!/usr/bin/env bash
# Bash completion for arm-cli
# Auto-generated from CLI structure - DO NOT EDIT MANUALLY
# Regenerate with: arm-cli system setup
# Enabled for: {aliases_comment}

_arm_cli_completion() {{
    local cur prev words cword
    COMPREPLY=()
    
    # Get current completion context
    _get_comp_words_by_ref -n : cur prev words cword 2>/dev/null || {{
        cur="${{COMP_WORDS[COMP_CWORD]}}"
        prev="${{COMP_WORDS[COMP_CWORD-1]}}"
        words=("${{COMP_WORDS[@]}}")
        cword=$COMP_CWORD
    }}
    
"""

    # Add command definitions
    for key, cmds in sorted(commands.items()):
        var_name = key.replace(".", "_") if key else "top"
        cmd_list = " ".join(cmds)
        script += f'    local {var_name}_commands="{cmd_list}"\n'

    # Add flag definitions
    for key, flgs in sorted(flags.items()):
        if flgs:  # Only add if there are flags
            var_name = key.replace(".", "_") if key else "top"
            flag_list = " ".join(flgs)
            script += f'    local {var_name}_flags="{flag_list}"\n'

    script += """
    # Build command path to determine context
    local cmd_path=""
    local i
    for ((i=1; i<cword; i++)); do
        case "${words[i]}" in
            -*) continue ;;  # Skip flags
            *)
                if [ -n "$cmd_path" ]; then
                    cmd_path="${cmd_path}.${words[i]}"
                else
                    cmd_path="${words[i]}"
                fi
                ;;
        esac
    done
    
    # Only show flags if user typed '-'
    local show_flags=0
    if [[ "${cur}" == -* ]]; then
        show_flags=1
    fi
    
    # Determine which commands and flags to show
    local available_commands=""
    local available_flags=""
    
    if [ -z "$cmd_path" ]; then
        available_commands="${top_commands}"
        available_flags="${top_flags:-}"
    else
        local var_name="${cmd_path//./_}_commands"
        local flag_var_name="${cmd_path//./_}_flags"
        available_commands="${!var_name}"
        available_flags="${!flag_var_name:-}"
    fi
    
    # If user typed '-', show flags; otherwise show commands
    if [ $show_flags -eq 1 ]; then
        available_commands="$available_flags"
    fi
    
    # Complete
    if [ -n "$available_commands" ]; then
        COMPREPLY=( $(compgen -W "${available_commands}" -- "${cur}") )
    fi
    
    # Handle special cases for file/directory arguments
    if [ ${#COMPREPLY[@]} -eq 0 ]; then
        case "${prev}" in
            --directory|--source|--path)
                COMPREPLY=( $(compgen -d -- "${cur}") )
                ;;
        esac
    fi
    
    return 0
}

"""

    # Register completion for all aliases
    for alias in aliases:
        script += f"complete -F _arm_cli_completion {alias}\n"

    return script


if __name__ == "__main__":
    print(generate_completion_script())
