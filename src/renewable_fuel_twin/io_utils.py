from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def write_json(path: Path, payload: Any) -> None:
    """
    Write a JSON-serializable object to the given file path as pretty-printed JSON, creating parent directories if needed.
    
    Parameters:
        path (Path): Destination file path; parent directories will be created if they do not exist.
        payload (Any): JSON-serializable object to write; the file is overwritten with an indented (2 spaces) JSON representation.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def write_yaml(path: Path, payload: Any) -> None:
    """
    Write the given Python object to the specified file as YAML, creating parent directories if they do not exist.
    
    The payload is serialized with yaml.safe_dump and written to the file at path; mapping key order is preserved (sort_keys=False).
    
    Parameters:
        path (Path): Destination file path where the YAML will be written.
        payload (Any): Python object to serialize to YAML.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False))
