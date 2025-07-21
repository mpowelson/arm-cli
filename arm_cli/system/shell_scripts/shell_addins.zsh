
# Setup autocomplete
eval "$(_ARM_CLI_COMPLETE=zsh_source arm-cli)"

# Export for use when launching Docker to match host file ownership
export CURRENT_UID=$(id -u):$(id -g)
