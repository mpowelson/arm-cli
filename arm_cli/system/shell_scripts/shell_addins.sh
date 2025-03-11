
## Setup autocomplete
# TODO: We can speed this up by generating the script offline. See https://click.palletsprojects.com/en/stable/shell-completion/
if type arm-cli >/dev/null 2>&1; then
    eval "$(_ARM_CLI_COMPLETE=source arm-cli)"  # TODO: This needs to change to eval "$(_ARM_CLI_COMPLETE=source arm-cli)" at some version.
fi


## Setup alias
alias_name="aa"
cli_path=$(which arm-cli)

# Create the alias if the cli was found
# TODO: Unfortunately, tab complete doesn't work when using the alias. Need to investigate a workaround
if [ -n "$cli_path" ]; then
  alias $alias_name='$cli_path'
fi

