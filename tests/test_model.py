from pathlib import Path

from renewable_fuel_twin.config import load_app_config, load_scenario_config
from renewable_fuel_twin.model import run_scenario
from renewable_fuel_twin.world_builder import build_world


def test_run_scenario(tmp_path):
    world = build_world(Path("data/seeds"), load_app_config(Path("configs/base.yaml")))
    result = run_scenario(world, load_app_config(Path("configs/base.yaml")), load_scenario_config(Path("configs/scenario_baseline.yaml")), output_root=tmp_path)
    assert (result["run_dir"] / "report.md").exists()
