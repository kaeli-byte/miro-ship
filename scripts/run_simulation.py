#!/usr/bin/env python
from pathlib import Path
import argparse

from renewable_fuel_twin.config import load_app_config, load_scenario_config
from renewable_fuel_twin.model import run_scenario
from renewable_fuel_twin.world_builder import build_world


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-dir", default="data/seeds")
    parser.add_argument("--config", default="configs/base.yaml")
    parser.add_argument("--scenario", required=True)
    args = parser.parse_args()

    world = build_world(Path(args.seed_dir), load_app_config(Path(args.config)))
    result = run_scenario(world, load_app_config(Path(args.config)), load_scenario_config(Path(args.scenario)))
    print(result["run_dir"])


if __name__ == "__main__":
    main()
