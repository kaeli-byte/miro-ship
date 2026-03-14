from __future__ import annotations

from dataclasses import dataclass

from .schemas import ScenarioConfig


@dataclass
class ScenarioRuntime:
    name: str
    steps: int
    interventions: list[dict]


def apply_scenario(base_steps: int, scenario: ScenarioConfig) -> ScenarioRuntime:
    steps = int(scenario.overrides.get("simulation", {}).get("steps", base_steps))
    return ScenarioRuntime(name=scenario.name, steps=steps, interventions=scenario.interventions)
