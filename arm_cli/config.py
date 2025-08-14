import json
from pathlib import Path

import appdirs
from pydantic import BaseModel


class Config(BaseModel):
    """Configuration schema for the CLI."""

    active_project: str = ""


def get_config_dir() -> Path:
    """Get the configuration directory for the CLI."""
    config_dir = Path(appdirs.user_config_dir("arm-cli"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / "config.json"


def load_config() -> Config:
    """Load configuration from file, creating default if it doesn't exist."""
    config_file = get_config_file()

    if not config_file.exists():
        # Create default config
        default_config = Config()
        save_config(default_config)
        return default_config

    try:
        with open(config_file, "r") as f:
            data = json.load(f)
        return Config(**data)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        # If config is corrupted, create a new one
        print(f"Warning: Config file corrupted, creating new default config: " f"{e}")
        default_config = Config()
        save_config(default_config)
        return default_config


def save_config(config: Config) -> None:
    """Save configuration to file."""
    config_file = get_config_file()

    # Ensure directory exists
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, "w") as f:
        json.dump(config.model_dump(), f, indent=2)
