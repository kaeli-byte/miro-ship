#!/usr/bin/env python
from pathlib import Path
import argparse
import json

from renewable_fuel_twin.config import load_app_config
from renewable_fuel_twin.world_builder import build_world


def main() -> None:
    """
    Builds a world from seed data and configuration, serializes its entities, and writes them as pretty-printed JSON to a file.
    
    Parses command-line arguments:
    - --seed-dir: path to the directory containing seed data (required)
    - --config: path to the application configuration file (required)
    - --output: path to write the JSON output (defaults to "outputs/world.json")
    
    Ensures the output directory exists, writes the serialized world entities to the output file, and prints the output path.
    """
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
