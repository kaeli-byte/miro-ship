from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InterventionError


@dataclass
class Intervention:
    id: str
    intervention_type: str
    target_ids: list[str]
    start_step: int
    end_step: int | None
    parameters: dict

    def active(self, step: int) -> bool:
        """
        Determine whether this intervention is active at the given simulation step.
        
        Parameters:
            step (int): Simulation step to evaluate.
        
        Returns:
            `true` if `step` is greater than or equal to `start_step` and less than or equal to `end_step` (or if `end_step` is `None`), `false` otherwise.
        """
        return self.start_step <= step and (self.end_step is None or step <= self.end_step)

    def apply(self, world, model) -> None:
        """
        Apply the intervention's effects to the simulation world and model.
        
        Parameters:
            world: The simulation state containing entities (e.g., ports, suppliers) that the intervention may modify.
            model: The scenario/model state (e.g., prices, supply limits) that the intervention may modify.
        
        Raises:
            NotImplementedError: If the base implementation is called instead of an override in a subclass.
        """
        raise NotImplementedError


class CarbonPriceShock(Intervention):
    def apply(self, world, model) -> None:
        """
        Update the model's carbon price from this intervention's parameters.
        
        Reads the "new_price_usd_per_tco2" parameter, converts it to a float, and assigns it to model.carbon_price.
        """
        model.carbon_price = float(self.parameters["new_price_usd_per_tco2"])


class PortDelayIntervention(Intervention):
    def apply(self, world, model) -> None:
        """
        Remove a specified fuel from the supported fuels list of targeted ports.
        
        Reads "fuel_id" from this intervention's parameters and, for each port in world.entities["ports"] whose id is listed in this intervention's target_ids and that currently supports the fuel, removes that fuel from the port's supported_fuels.
        """
        fuel_id = self.parameters["fuel_id"]
        for port in world.entities["ports"]:
            if port.id in self.target_ids and fuel_id in port.supported_fuels:
                port.supported_fuels.remove(fuel_id)


class FuelSupplyDisruption(Intervention):
    def apply(self, world, model) -> None:
        """
        Apply a capacity multiplier to a supplier's maximum supply for a specified fuel.
        
        Uses `parameters["supplier_id"]`, `parameters["fuel_id"]`, and `parameters["capacity_multiplier"]` to multiply the matching supplier's `max_supply_by_fuel[fuel_id]` by the numeric multiplier.
        
        Raises:
            InterventionError: If no supplier with `parameters["supplier_id"]` exists in `world.entities["suppliers"]`.
        """
        supplier_id = self.parameters["supplier_id"]
        fuel_id = self.parameters["fuel_id"]
        mult = float(self.parameters["capacity_multiplier"])
        for supplier in world.entities["suppliers"]:
            if supplier.id == supplier_id:
                supplier.max_supply_by_fuel[fuel_id] *= mult
                return
        raise InterventionError(f"supplier not found: {supplier_id}")


def build_interventions(specs: list[dict]) -> list[Intervention]:
    """
    Create Intervention instances from specification dictionaries.
    
    Parameters:
        specs (list[dict]): List of intervention specification dictionaries. Each spec must include an "intervention_type" key whose value is one of "CarbonPriceShock", "PortDelayIntervention", or "FuelSupplyDisruption", and keys matching the Intervention dataclass constructor (e.g., "id", "target_ids", "start_step", "end_step", "parameters").
    
    Returns:
        list[Intervention]: A list of instantiated Intervention subclasses corresponding to each specification.
    """
    mapping = {
        "CarbonPriceShock": CarbonPriceShock,
        "PortDelayIntervention": PortDelayIntervention,
        "FuelSupplyDisruption": FuelSupplyDisruption,
    }
    return [mapping[s["intervention_type"]](**s) for s in specs]
