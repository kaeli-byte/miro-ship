from renewable_fuel_twin.agents import ShipOperatorAgent
from renewable_fuel_twin.memory import AgentMemory
from renewable_fuel_twin.personas import make_persona


def test_choose_fuel():
    agent = ShipOperatorAgent("o", AgentMemory(), ["a", "b"], make_persona("cost_minimizer_operator", ["a", "b"]))
    assert agent.choose_fuel({"a": 1.0, "b": 2.0}) == "b"
