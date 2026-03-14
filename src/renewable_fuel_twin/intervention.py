from __future__ import annotations

from dataclasses import dataclass, field

from .exceptions import InterventionError


@dataclass
class Intervention:
    id: str
    intervention_type: str
    target_ids: list[str]
    start_step: int
    end_step: int | None = None
    parameters: dict = field(default_factory=dict)

    def active(self, step: int) -> bool:
        return self.start_step <= step and (self.end_step is None or step <= self.end_step)

    def apply(self, world, model) -> None:
        raise NotImplementedError

    def revert(self, world, model) -> None:
        raise NotImplementedError


class CarbonPriceShock(Intervention):
    def apply(self, world, model) -> None:
        if not hasattr(self, "_original_carbon_price"):
            self._original_carbon_price = model.carbon_price
        model.carbon_price = float(self.parameters["new_price_usd_per_tco2"])

    def revert(self, world, model) -> None:
        if not hasattr(self, "_original_carbon_price"):
            return
        model.carbon_price = self._original_carbon_price
        del self._original_carbon_price


class PortDelayIntervention(Intervention):
    def apply(self, world, model) -> None:
        if not hasattr(self, "_original_supported_fuels"):
            self._original_supported_fuels = {}
        fuel_id = self.parameters["fuel_id"]
        for port in world.entities["ports"]:
            if port.id in self.target_ids:
                if port.id not in self._original_supported_fuels:
                    self._original_supported_fuels[port.id] = list(port.supported_fuels)
                if fuel_id in port.supported_fuels:
                    port.supported_fuels.remove(fuel_id)

    def revert(self, world, model) -> None:
        if not hasattr(self, "_original_supported_fuels"):
            return
        for port in world.entities["ports"]:
            original_supported_fuels = self._original_supported_fuels.get(port.id)
            if original_supported_fuels is not None:
                port.supported_fuels = list(original_supported_fuels)
        del self._original_supported_fuels


class FuelSupplyDisruption(Intervention):
    def apply(self, world, model) -> None:
        supplier_id = self.parameters["supplier_id"]
        fuel_id = self.parameters["fuel_id"]
        mult = float(self.parameters["capacity_multiplier"])
        for supplier in world.entities["suppliers"]:
            if supplier.id == supplier_id:
                if fuel_id not in supplier.max_supply_by_fuel:
                    raise InterventionError(
                        f"fuel not found for supplier: supplier_id={supplier_id}, fuel_id={fuel_id}"
                    )
                if not hasattr(self, "_original_max_supply"):
                    self._original_max_supply = supplier.max_supply_by_fuel[fuel_id]
                supplier.max_supply_by_fuel[fuel_id] *= mult
                return
        raise InterventionError(f"supplier not found: {supplier_id}")

    def revert(self, world, model) -> None:
        if not hasattr(self, "_original_max_supply"):
            return
        supplier_id = self.parameters["supplier_id"]
        fuel_id = self.parameters["fuel_id"]
        for supplier in world.entities["suppliers"]:
            if supplier.id == supplier_id:
                supplier.max_supply_by_fuel[fuel_id] = self._original_max_supply
                del self._original_max_supply
                return
        raise InterventionError(f"supplier not found: {supplier_id}")


def build_interventions(specs: list[dict]) -> list[Intervention]:
    mapping = {
        "CarbonPriceShock": CarbonPriceShock,
        "PortDelayIntervention": PortDelayIntervention,
        "FuelSupplyDisruption": FuelSupplyDisruption,
    }
    interventions: list[Intervention] = []
    for spec in specs:
        intervention_type = spec.get("intervention_type")
        cls = mapping.get(intervention_type)
        if cls is None:
            raise ValueError(f"Unknown intervention_type '{intervention_type}' in spec: {spec}")
        interventions.append(cls(**spec))
    return interventions
