from __future__ import annotations

from dataclasses import dataclass

from .memory import AgentMemory
from .personas import Persona


@dataclass
class BaseAgent:
    id: str
    memory: AgentMemory


@dataclass
class ShipOperatorAgent(BaseAgent):
    preferred_fuels: list[str]
    persona: Persona

    def choose_fuel(self, scores: dict[str, float]) -> str:
        """
        Selects the fuel key with the highest score from a mapping of fuel scores.
        
        Parameters:
            scores (dict[str, float]): Mapping from fuel identifier to its numeric score.
        
        Returns:
            str: The fuel identifier with the highest score. If multiple fuels share the highest score, one of them (the first encountered) is returned.
        """
        return max(scores, key=scores.get)


@dataclass
class RegulatorAgent(BaseAgent):
    carbon_price: float


@dataclass
class FuelSupplierAgent(BaseAgent):
    price_markup: float


@dataclass
class PortAgent(BaseAgent):
    supported_fuels: list[str]


@dataclass
class CargoOwnerAgent(BaseAgent):
    premium_tolerance: float
