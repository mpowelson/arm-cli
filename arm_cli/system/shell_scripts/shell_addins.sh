
## Setup autocomplete
# TODO: We can speed this up by generating the script offline. See https://click.palletsprojects.com/en/stable/shell-completion/
if type arm-cli >/dev/null 2>&1; then
    eval "$(_ARM_CLI_COMPLETE=bash_source arm-cli)"
fi


## Setup alias
alias_name="aa"
cli_path=$(which arm-cli)

# Create the alias if the cli was found
if [ -n "$cli_path" ]; then
  alias $alias_name="$cli_path"
fi

# TODO: Figure out tab complete for the alias

# Export for use when launching Docker to match host file ownership
export CURRENT_UID=$(id -u):$(id -g)
