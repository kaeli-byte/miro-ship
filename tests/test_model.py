from pathlib import Path

from renewable_fuel_twin.config import load_app_config, load_scenario_config
from renewable_fuel_twin.model import run_scenario
from renewable_fuel_twin.world_builder import build_world


def test_run_scenario(tmp_path):
    app_config = load_app_config(Path("configs/base.yaml"))
    world = build_world(Path("data/seeds"), app_config)
    result = run_scenario(world, app_config, load_scenario_config(Path("configs/scenario_baseline.yaml")), output_root=tmp_path)
    assert (result["run_dir"] / "report.md").exists()
