from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NormalizedSeeds:
    entities: dict
    relationships: list[dict]
    assumptions: list[str]
    events: list[dict]


def normalize_seed_materials(seeds: dict) -> NormalizedSeeds:
    """
    Normalize raw seed materials into a NormalizedSeeds structure.
    
    This produces a NormalizedSeeds instance whose `entities` field contains the original `seeds` input and whose `relationships` field lists supplier-to-fuel@port relationship records. Each relationship record has `type` "supplier_offers_fuel_at_port", `source` set to the supplier's id, and `target` set to "<fuel>@<port>". The returned `assumptions` and `events` lists are empty.
    
    Parameters:
        seeds (dict): Input seed data. Expected to include a "suppliers" iterable where each supplier exposes `id`, `fuel_ids` (iterable of fuel identifiers), and `port_ids` (iterable of port identifiers).
    
    Returns:
        NormalizedSeeds: A NormalizedSeeds object containing the original entities, generated relationships, and empty `assumptions` and `events`.
    """
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
