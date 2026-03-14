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
    parser.add_argument("--scenarios", nargs="+", required=True)
    args = parser.parse_args()

    app_config = load_app_config(Path(args.config))
    world = build_world(Path(args.seed_dir), app_config)
    for scenario in args.scenarios:
        run_scenario(world, app_config, load_scenario_config(Path(scenario)))
    print("batch complete")


if __name__ == "__main__":
    main()
