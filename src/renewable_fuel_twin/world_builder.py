from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import networkx as nx

from .config import load_app_config
from .exceptions import WorldBuildError
from .schemas import AppConfig
from .seed_ingestion import load_seed_entities


@dataclass
class World:
    entities: dict
    graph: nx.MultiDiGraph


REQUIRED = ("fuels", "ports", "routes", "operators", "suppliers", "cargo_owners", "policies")


def build_world(seed_dir: Path, config: AppConfig) -> World:
    seeds = load_seed_entities(seed_dir)
    for name in REQUIRED:
        if name not in seeds:
            raise WorldBuildError(f"missing seed category: {name}")

    graph = nx.MultiDiGraph()
    fuel_ids = {f.id for f in seeds["fuels"]}
    port_ids = {p.id for p in seeds["ports"]}

    for group in seeds.values():
        for item in group:
            graph.add_node(item.id, type=item.__class__.__name__)

    for route in seeds["routes"]:
        if route.origin_port_id not in port_ids or route.destination_port_id not in port_ids:
            raise WorldBuildError("route references unknown port")
        graph.add_edge(route.origin_port_id, route.destination_port_id, relation="route_connects_ports", route_id=route.id)

    for port in seeds["ports"]:
        for fuel_id in port.supported_fuels:
            if fuel_id not in fuel_ids:
                raise WorldBuildError(f"unsupported fuel reference: {fuel_id}")
            graph.add_edge(port.id, fuel_id, relation="port_supports_fuel")

    for supplier in seeds["suppliers"]:
        for fuel_id in supplier.fuel_ids:
            if fuel_id not in fuel_ids:
                raise WorldBuildError(f"unsupported fuel reference: {fuel_id}")
            for port_id in supplier.port_ids:
                if port_id not in port_ids:
                    raise WorldBuildError(f"missing port reference: {port_id}")
                graph.add_edge(supplier.id, f"{fuel_id}@{port_id}", relation="supplier_offers_fuel_at_port")

    _ = config  # reserved for future schema defaults
    return World(entities=seeds, graph=graph)


def build_world_from_paths(seed_dir: Path, config_path: Path) -> World:
    return build_world(seed_dir, load_app_config(config_path))
