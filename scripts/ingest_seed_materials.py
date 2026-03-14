#!/usr/bin/env python
from pathlib import Path
import argparse

from renewable_fuel_twin.seed_ingestion import load_seed_entities


def main() -> None:
    """
    Run a CLI that loads seed entities from a directory and prints counts per entity type.
    
    This function parses a single optional `--seed-dir` argument (default "data/seeds"), loads seed entities from that directory via `load_seed_entities`, and prints a mapping of each entity key to the number of items loaded.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-dir", default="data/seeds")
    args = parser.parse_args()
    entities = load_seed_entities(Path(args.seed_dir))
    print({k: len(v) for k, v in entities.items()})


if __name__ == "__main__":
    main()
