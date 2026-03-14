from pathlib import Path

from renewable_fuel_twin.config import load_app_config
from renewable_fuel_twin.world_builder import build_world


def test_build_world_graph_nodes():
    world = build_world(Path("data/seeds"), load_app_config(Path("configs/base.yaml")))
    assert world.graph.number_of_nodes() > 0
