from __future__ import annotations

import csv
import json
from collections.abc import Sequence
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
    suffix = path.suffix.lower()
    raw = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(raw)
    if suffix == ".json":
        return json.loads(raw)
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    raise ValueError(f"Unsupported seed format: {path}")


def load_seed_entities(seed_dir: Path) -> dict[str, list]:
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
        if items is None:
            items = []
        if isinstance(items, (str, bytes)) or not isinstance(items, Sequence):
            raise ValueError(f"Malformed seed data in {path}: expected a sequence of items")
        result[name] = [schema.model_validate(i) for i in items]
    return result
