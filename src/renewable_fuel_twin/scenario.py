from __future__ import annotations

from dataclasses import dataclass

from .schemas import ScenarioConfig


@dataclass
class ScenarioRuntime:
    name: str
    steps: int
    interventions: list[dict]


def apply_scenario(base_steps: int, scenario: ScenarioConfig) -> ScenarioRuntime:
    """
    Create a ScenarioRuntime from a ScenarioConfig, using an override step count when provided.
    
    Parameters:
        base_steps (int): Default number of steps to use if the scenario does not specify one.
        scenario (ScenarioConfig): Scenario configuration to convert.
    
    Returns:
        ScenarioRuntime: Instance whose name is taken from `scenario.name`, whose `steps` is `scenario.overrides["simulation"]["steps"]` converted to int when present (otherwise `base_steps`), and whose `interventions` is `scenario.interventions`.
    """
    steps = int(scenario.overrides.get("simulation", {}).get("steps", base_steps))
    return ScenarioRuntime(name=scenario.name, steps=steps, interventions=scenario.interventions)
