#!/usr/bin/env python
from pathlib import Path
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if run_dir.name == "latest":
        run_dir = (run_dir.parent / run_dir.readlink()).resolve()
    print((run_dir / "report.md").read_text())


if __name__ == "__main__":
    main()
