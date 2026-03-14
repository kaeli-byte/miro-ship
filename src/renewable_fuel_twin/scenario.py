from __future__ import annotations

from dataclasses import dataclass
from numbers import Number

from .schemas import ScenarioConfig


@dataclass
class ScenarioRuntime:
    name: str
    steps: int
    interventions: list[dict]


def apply_scenario(base_steps: int, scenario: ScenarioConfig) -> ScenarioRuntime:
    sim_overrides = scenario.overrides.get("simulation", {})
    if not isinstance(sim_overrides, dict):
        raise ValueError(f"Invalid simulation overrides for scenario '{scenario.name}': {sim_overrides}")

    raw_steps = sim_overrides.get("steps", base_steps)
    try:
        if isinstance(raw_steps, Number):
            steps = int(raw_steps)
        elif isinstance(raw_steps, str) and raw_steps.strip().isdigit():
            steps = int(raw_steps.strip())
        else:
            raise ValueError
    except ValueError as exc:
        raise ValueError(f"Invalid steps override for scenario '{scenario.name}': {raw_steps}") from exc

    if steps <= 0:
        raise ValueError(f"Invalid steps override for scenario '{scenario.name}': {raw_steps}")

    return ScenarioRuntime(name=scenario.name, steps=steps, interventions=scenario.interventions)
