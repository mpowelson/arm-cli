
## Setup autocomplete
# TODO: We can speed this up by generating the script offline. See https://click.palletsprojects.com/en/stable/shell-completion/
if type arm-cli >/dev/null 2>&1; then
    eval "$(_ARM_CLI_COMPLETE=source arm-cli)"  # TODO: This needs to change to eval "$(_ARM_CLI_COMPLETE=source arm-cli)" at some version.
fi
