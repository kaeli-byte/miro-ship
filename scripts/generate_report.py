#!/usr/bin/env python
from pathlib import Path
import argparse


def main() -> None:
    """
    Prints the contents of report.md for a specified run directory.
    
    Parses the required command-line argument `--run-dir`. If the provided path's final component is "latest",
    the script resolves that symlink relative to its parent directory and uses the resolved directory.
    Reads report.md from the resolved run directory and writes its contents to standard output.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if run_dir.name == "latest":
        run_dir = (run_dir.parent / run_dir.readlink()).resolve()
    print((run_dir / "report.md").read_text())


if __name__ == "__main__":
    main()
