from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from .schemas import (
    CargoOwnerSchema,
    FuelSchema,
    PolicySchema,
    PortSchema,
    RouteSchema,
    ShipOperatorSchema,
    SupplierSchema,
)


def _read_any(path: Path) -> Any:
    """
    Read a file and parse its contents based on the file's suffix.
    
    Parameters:
        path (Path): Path to the input file. Supported suffixes: `.yaml`, `.yml`, `.json`, `.csv`.
    
    Returns:
        Any: Parsed Python representation of the file contents. For YAML/JSON this is the object produced by the parser (typically a dict or list); for CSV this is a list of dictionaries mapping column names to string values.
    
    Raises:
        ValueError: If the file suffix is not one of the supported formats.
    """
    suffix = path.suffix.lower()
    raw = path.read_text()
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(raw)
    if suffix == ".json":
        return json.loads(raw)
    if suffix == ".csv":
        with path.open(newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError(f"Unsupported seed format: {path}")


def load_seed_entities(seed_dir: Path) -> dict[str, list]:
    """
    Load seed data files from a directory and return validated model instances grouped by entity type.
    
    Reads "{name}.yaml" files for each supported seed category in the given directory, validates and converts each record using the corresponding schema, and returns a dictionary mapping category names (e.g., "fuels", "ports") to lists of validated model instances.
    
    Parameters:
    	seed_dir (Path): Directory containing seed files named "<category>.yaml" for each supported category.
    
    Returns:
    	dict[str, list]: Mapping from seed category name to a list of validated model instances for that category.
    """
    mapping = {
        "fuels": FuelSchema,
        "ports": PortSchema,
        "routes": RouteSchema,
        "operators": ShipOperatorSchema,
        "suppliers": SupplierSchema,
        "cargo_owners": CargoOwnerSchema,
        "policies": PolicySchema,
    }
    result: dict[str, list] = {}
    for name, schema in mapping.items():
        path = seed_dir / f"{name}.yaml"
        items = _read_any(path)
        result[name] = [schema.model_validate(i) for i in items]
    return result
