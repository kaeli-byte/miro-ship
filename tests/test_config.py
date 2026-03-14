from pathlib import Path

from renewable_fuel_twin.config import load_app_config


def test_load_app_config():
    cfg = load_app_config(Path("configs/base.yaml"))
    assert cfg.simulation.steps == 12
