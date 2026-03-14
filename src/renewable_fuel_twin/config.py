from pathlib import Path

import yaml

from .exceptions import ConfigValidationError
from .schemas import AppConfig, ScenarioConfig


def _read_yaml(path: Path) -> dict:
    """
    Read a YAML file from the given path and return its contents as a dictionary.
    
    Parameters:
        path (Path): Filesystem path to the YAML configuration file.
    
    Returns:
        dict: Parsed YAML content as a dictionary; returns an empty dict if the file is empty or parses to a falsy value.
    
    Raises:
        ConfigValidationError: If the file at `path` does not exist.
    """
    if not path.exists():
        raise ConfigValidationError(f"Config file not found: {path}")
    return yaml.safe_load(path.read_text()) or {}


def load_app_config(path: Path) -> AppConfig:
    """
    Load and validate application configuration from a YAML file.
    
    Parameters:
        path (Path): Path to the YAML configuration file.
    
    Returns:
        AppConfig: Validated application configuration object.
    
    Raises:
        ConfigValidationError: If the file cannot be read or the contents fail schema validation; the original error message is preserved.
    """
    try:
        return AppConfig.model_validate(_read_yaml(path))
    except Exception as exc:
        raise ConfigValidationError(str(exc)) from exc


def load_scenario_config(path: Path) -> ScenarioConfig:
    """
    Load and validate a scenario configuration from a YAML file.
    
    Parameters:
        path (Path): Filesystem path to the YAML file containing the scenario configuration.
    
    Returns:
        ScenarioConfig: The validated scenario configuration object.
    
    Raises:
        ConfigValidationError: If the file is missing, cannot be parsed, or fails schema validation.
    """
    try:
        return ScenarioConfig.model_validate(_read_yaml(path))
    except Exception as exc:
        raise ConfigValidationError(str(exc)) from exc
