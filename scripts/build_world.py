#!/usr/bin/env python
from pathlib import Path
import argparse
import json

from renewable_fuel_twin.config import load_app_config
from renewable_fuel_twin.world_builder import build_world


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-dir", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="outputs/world.json")
    args = parser.parse_args()

    world = build_world(Path(args.seed_dir), load_app_config(Path(args.config)))
    payload = {k: [x.model_dump() for x in v] for k, v in world.entities.items()}
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(payload, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
