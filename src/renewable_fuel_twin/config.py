from pathlib import Path

import yaml

from .exceptions import ConfigValidationError
from .schemas import AppConfig, ScenarioConfig


def _read_yaml(path: Path) -> dict:
    if not path.exists():
        raise ConfigValidationError(f"Config file not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_app_config(path: Path) -> AppConfig:
    try:
        return AppConfig.model_validate(_read_yaml(path))
    except Exception as exc:
        raise ConfigValidationError(f"error validating {path}: {exc}") from exc


def load_scenario_config(path: Path) -> ScenarioConfig:
    try:
        return ScenarioConfig.model_validate(_read_yaml(path))
    except Exception as exc:
        raise ConfigValidationError(f"error validating {path}: {exc}") from exc
