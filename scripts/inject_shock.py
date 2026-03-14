#!/usr/bin/env python
from pathlib import Path
import argparse
import yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--shock-json", required=True)
    args = parser.parse_args()

    path = Path(args.scenario)
    data = yaml.safe_load(path.read_text())
    data.setdefault("interventions", []).append(yaml.safe_load(args.shock_json))
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    print(path)


if __name__ == "__main__":
    main()
