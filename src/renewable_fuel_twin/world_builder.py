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
    """
    Constructs a World graph from seed entities in seed_dir and validates inter-entity references.
    
    Parameters:
        seed_dir (Path): Directory containing seed entity definitions to load.
        config (AppConfig): Application configuration (currently reserved for future defaults).
    
    Returns:
        World: A World dataclass containing the loaded entities and a NetworkX MultiDiGraph where:
            - Nodes represent each seed entity with a `type` attribute set to the entity class name.
            - Edges represent relationships:
                - relation="route_connects_ports" between origin and destination ports for each route.
                - relation="port_supports_fuel" from a port to each supported fuel.
                - relation="supplier_offers_fuel_at_port" from a supplier to composite nodes of the form "<fuel_id>@<port_id>".
    
    Raises:
        WorldBuildError: If required seed categories are missing, if a route references an unknown port,
                        if a port or supplier references an unknown fuel, or if a supplier references an unknown port.
    """
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
    """
    Builds a World from seed files and an application configuration file.
    
    Parameters:
    	seed_dir (Path): Directory containing seed entity files.
    	config_path (Path): Path to the application configuration file used to configure world construction.
    
    Returns:
    	world (World): A World instance containing the loaded entities and the constructed graph.
    """
    return build_world(seed_dir, load_app_config(config_path))
