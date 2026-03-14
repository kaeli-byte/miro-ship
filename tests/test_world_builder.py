from pathlib import Path

import yaml

from renewable_fuel_twin.config import load_app_config
from renewable_fuel_twin.world_builder import build_world


def test_build_world_graph_nodes(tmp_path):
    seed_dir = tmp_path / "seeds"
    seed_dir.mkdir()
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "simulation": {"steps": 2, "seed": 1},
                "carbon_price_usd_per_tco2": 10,
                "transport_premium": 1,
                "port_fee": 1,
            }
        ),
        encoding="utf-8",
    )

    (seed_dir / "fuels.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "f1",
                    "name": "Fuel1",
                    "base_price_usd_per_tonne": 100,
                    "emission_factor_tco2e_per_tonne": 1,
                    "infra_maturity_score": 0.8,
                    "operational_risk_score": 0.2,
                    "supply_elasticity": 0.5,
                }
            ]
        ),
        encoding="utf-8",
    )
    (seed_dir / "ports.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "p1",
                    "name": "Port1",
                    "region": "R",
                    "supported_fuels": ["f1"],
                    "bunkering_capacity_by_fuel": {"f1": 1000},
                    "expansion_threshold": 0.8,
                    "expansion_delay_steps": 1,
                }
            ]
        ),
        encoding="utf-8",
    )
    (seed_dir / "routes.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "r1",
                    "origin_port_id": "p1",
                    "destination_port_id": "p1",
                    "distance_nm": 10,
                    "disruption_risk_score": 0.1,
                }
            ]
        ),
        encoding="utf-8",
    )
    (seed_dir / "operators.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "o1",
                    "name": "Op1",
                    "fleet_size": 1,
                    "route_ids": ["r1"],
                    "risk_tolerance": 0.5,
                    "green_premium_tolerance": 10,
                    "preferred_fuels": ["f1"],
                    "retrofit_budget": 10,
                }
            ]
        ),
        encoding="utf-8",
    )
    (seed_dir / "suppliers.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "s1",
                    "name": "S1",
                    "fuel_ids": ["f1"],
                    "port_ids": ["p1"],
                    "max_supply_by_fuel": {"f1": 100},
                    "reliability_score": 0.9,
                    "price_markup": 5,
                }
            ]
        ),
        encoding="utf-8",
    )
    (seed_dir / "cargo_owners.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "c1",
                    "name": "C1",
                    "preferred_emission_intensity": 1,
                    "willingness_to_pay_green_premium": 5,
                    "contracted_route_ids": ["r1"],
                }
            ]
        ),
        encoding="utf-8",
    )
    (seed_dir / "policies.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "id": "pcy1",
                    "type": "carbon_price",
                    "region": "global",
                    "start_step": 0,
                    "end_step": None,
                    "parameters": {"carbon_price_usd_per_tco2": 10},
                }
            ]
        ),
        encoding="utf-8",
    )

    world = build_world(seed_dir, load_app_config(config_path))
    assert world.graph.number_of_nodes() == 8
    assert world.graph.has_node("f1@p1")
    assert world.graph.nodes["f1@p1"]["type"] == "fuel_at_port"
