#!/usr/bin/env python
from pathlib import Path
import argparse
import shutil
import yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, help="Path to scenario YAML to modify in place unless --dry-run is set")
    parser.add_argument("--shock-json", required=True, help="YAML/JSON object string to append to scenario interventions")
    parser.add_argument("--dry-run", action="store_true", help="Print updated scenario without writing to disk")
    parser.add_argument("--backup", action="store_true", help="Create a .bak backup before writing")
    args = parser.parse_args()

    path = Path(args.scenario)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data.setdefault("interventions", []).append(yaml.safe_load(args.shock_json))
    rendered = yaml.safe_dump(data, sort_keys=False)

    if args.dry_run:
        print(rendered)
        return

    if args.backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup_path)

    path.write_text(rendered, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
