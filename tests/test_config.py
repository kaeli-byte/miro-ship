from pathlib import Path

import pytest

from renewable_fuel_twin.config import load_app_config
from renewable_fuel_twin.exceptions import ConfigValidationError


def test_load_app_config():
    cfg = load_app_config(Path("configs/base.yaml"))
    assert cfg.simulation.steps == 12


def test_load_app_config_invalid_raises(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("carbon_price_usd_per_tco2: 50\n", encoding="utf-8")
    with pytest.raises(ConfigValidationError):
        load_app_config(bad)
