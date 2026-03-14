from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class FuelSchema(BaseModel):
    id: str
    name: str
    base_price_usd_per_tonne: float
    emission_factor_tco2e_per_tonne: float
    infra_maturity_score: float = Field(ge=0, le=1)
    operational_risk_score: float = Field(ge=0, le=1)
    supply_elasticity: float


class PortSchema(BaseModel):
    id: str
    name: str
    region: str
    supported_fuels: list[str]
    bunkering_capacity_by_fuel: dict[str, float]
    expansion_threshold: float = Field(ge=0, le=1)
    expansion_delay_steps: int


class RouteSchema(BaseModel):
    id: str
    origin_port_id: str
    destination_port_id: str
    distance_nm: float
    disruption_risk_score: float = Field(ge=0, le=1)


class ShipOperatorSchema(BaseModel):
    id: str
    name: str
    fleet_size: int
    route_ids: list[str]
    risk_tolerance: float = Field(ge=0, le=1)
    green_premium_tolerance: float
    preferred_fuels: list[str]
    retrofit_budget: float


class SupplierSchema(BaseModel):
    id: str
    name: str
    fuel_ids: list[str]
    port_ids: list[str]
    max_supply_by_fuel: dict[str, float]
    reliability_score: float = Field(ge=0, le=1)
    price_markup: float


class CargoOwnerSchema(BaseModel):
    id: str
    name: str
    preferred_emission_intensity: float
    willingness_to_pay_green_premium: float
    contracted_route_ids: list[str]


class PolicySchema(BaseModel):
    id: str
    type: str
    region: str
    start_step: int
    end_step: int | None = None
    parameters: dict[str, float | str | bool]


class EventSchema(BaseModel):
    id: str
    step: int
    event_type: str
    actor_ids: list[str]
    payload: dict[str, Any]
    severity: float


class SimulationConfig(BaseModel):
    steps: int = Field(gt=0)
    seed: int


class AppConfig(BaseModel):
    simulation: SimulationConfig
    carbon_price_usd_per_tco2: float = 0
    transport_premium: float = 0
    port_fee: float = 0


class ScenarioConfig(BaseModel):
    name: str
    overrides: dict[str, Any] = {}
    interventions: list[dict[str, Any]] = []

    @field_validator("interventions")
    @classmethod
    def validate_interventions(cls, interventions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Validate that each intervention dictionary includes all required fields.
        
        Parameters:
            interventions (list[dict[str, Any]]): List of intervention dictionaries to validate. Each item must contain the keys "id", "intervention_type", "start_step", "parameters", and "target_ids".
        
        Returns:
            list[dict[str, Any]]: The original interventions list if all items are valid.
        
        Raises:
            ValueError: If any intervention is missing a required key; message is "missing intervention field: {required}" where {required} is the missing key.
        """
        for item in interventions:
            for required in ("id", "intervention_type", "start_step", "parameters", "target_ids"):
                if required not in item:
                    raise ValueError(f"missing intervention field: {required}")
        return interventions
