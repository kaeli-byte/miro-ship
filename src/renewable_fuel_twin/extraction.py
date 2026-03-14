from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NormalizedSeeds:
    entities: dict
    relationships: list[dict]
    assumptions: list[str]
    events: list[dict]


def normalize_seed_materials(seeds: dict) -> NormalizedSeeds:
    relationships: list[dict] = []
    for supplier in seeds["suppliers"]:
        for fuel in supplier.fuel_ids:
            for port in supplier.port_ids:
                relationships.append(
                    {
                        "type": "supplier_offers_fuel_at_port",
                        "source": supplier.id,
                        "target": f"{fuel}@{port}",
                    }
                )
    return NormalizedSeeds(entities=seeds, relationships=relationships, assumptions=[], events=[])
