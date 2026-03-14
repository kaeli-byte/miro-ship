#!/usr/bin/env python
from pathlib import Path
import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)

    if run_dir.name == "latest":
        if not run_dir.is_symlink():
            print(f"error: {run_dir} is not a symlink; pass outputs/runs/<run_id> explicitly", file=sys.stderr)
            raise SystemExit(1)
        try:
            run_dir = (run_dir.parent / run_dir.readlink()).resolve()
        except (OSError, ValueError) as exc:
            print(f"error: unable to resolve latest symlink {run_dir}: {exc}", file=sys.stderr)
            raise SystemExit(1)

    report_path = run_dir / "report.md"
    if not report_path.exists():
        print(f"error: report file not found: {report_path}", file=sys.stderr)
        raise SystemExit(1)

    print(report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
