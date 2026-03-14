import pytest

from renewable_fuel_twin.agents import ShipOperatorAgent
from renewable_fuel_twin.memory import AgentMemory
from renewable_fuel_twin.personas import make_persona


def test_choose_fuel():
    agent = ShipOperatorAgent("o", AgentMemory(), ["a", "b"], make_persona("cost_minimizer_operator", ["a", "b"]))
    assert agent.choose_fuel({"a": 1.0, "b": 2.0}) == "b"


def test_choose_fuel_empty_scores_raises():
    agent = ShipOperatorAgent("o", AgentMemory(), [], make_persona("cost_minimizer_operator", ["a", "b"]))
    with pytest.raises(ValueError, match="no candidate fuels"):
        agent.choose_fuel({})
