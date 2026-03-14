#!/usr/bin/env python
from pathlib import Path
import argparse
import yaml


def main() -> None:
    """
    Injects a YAML "shock" into a scenario file specified by command-line arguments.
    
    Reads the scenario file path from the `--scenario` argument and loads it as YAML, ensures the document has an "interventions" list (creating one if missing), appends the YAML parsed from the `--shock-json` argument to that list, writes the updated YAML back to the same file without sorting keys, and prints the scenario file path.
    """
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
