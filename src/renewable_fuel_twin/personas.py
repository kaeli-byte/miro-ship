from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Persona:
    name: str
    role: str
    risk_tolerance: float
    infra_confidence_by_fuel: dict[str, float]
    technology_sentiment_by_fuel: dict[str, float]
    policy_expectation_bias: float
    switching_inertia: float
    narrative_sensitivity: float


ARCHETYPES = {
    "conservative_operator": dict(role="ship_operator", risk_tolerance=0.2, policy_expectation_bias=0.6, switching_inertia=0.8, narrative_sensitivity=0.4),
    "aggressive_green_operator": dict(role="ship_operator", risk_tolerance=0.7, policy_expectation_bias=0.8, switching_inertia=0.3, narrative_sensitivity=0.7),
    "cost_minimizer_operator": dict(role="ship_operator", risk_tolerance=0.4, policy_expectation_bias=0.5, switching_inertia=0.6, narrative_sensitivity=0.3),
}


def make_persona(archetype: str, fuels: list[str], seed: int = 0) -> Persona:
    """
    Create a Persona instance from a named archetype and a list of fuels.
    
    Constructs a Persona whose role and behavioral parameters are taken from the selected archetype. A small bias derived from `seed` adjusts the persona's `risk_tolerance` (capped at 1.0) and increases `infra_confidence_by_fuel` for each fuel; `technology_sentiment_by_fuel` is initialized to 0.5 for each fuel. Other attributes (policy expectation bias, switching inertia, narrative sensitivity) are copied from the archetype.
    
    Parameters:
        archetype (str): Key of the archetype in ARCHETYPES.
        fuels (list[str]): Iterable of fuel identifiers to initialize per-fuel fields.
        seed (int): Integer seed that deterministically modifies the persona's bias.
    
    Returns:
        Persona: A Persona populated from the archetype with per-fuel confidences and sentiments.
    """
    data = ARCHETYPES[archetype]
    bias = (seed % 7) / 20
    return Persona(
        name=archetype,
        role=data["role"],
        risk_tolerance=min(1.0, data["risk_tolerance"] + bias),
        infra_confidence_by_fuel={f: 0.5 + bias for f in fuels},
        technology_sentiment_by_fuel={f: 0.5 for f in fuels},
        policy_expectation_bias=data["policy_expectation_bias"],
        switching_inertia=data["switching_inertia"],
        narrative_sensitivity=data["narrative_sensitivity"],
    )
