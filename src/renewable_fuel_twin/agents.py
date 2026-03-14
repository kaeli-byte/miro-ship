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
        if not scores:
            raise ValueError("no candidate fuels to select from")
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
