import pytest

from renewable_fuel_twin.exceptions import InterventionError
from renewable_fuel_twin.intervention import CarbonPriceShock, FuelSupplyDisruption, build_interventions


class M:
    def __init__(self):
        self.carbon_price = 0


class Supplier:
    def __init__(self, sid: str, supplies: dict[str, float]):
        self.id = sid
        self.max_supply_by_fuel = supplies


class W:
    def __init__(self, suppliers):
        self.entities = {"suppliers": suppliers}


def test_carbon_shock():
    i = CarbonPriceShock(id="x", intervention_type="CarbonPriceShock", target_ids=["global"], start_step=0, end_step=1, parameters={"new_price_usd_per_tco2": 100})
    m = M()
    i.apply(None, m)
    assert m.carbon_price == 100


def test_build_intervention_defaults_end_step_when_omitted():
    interventions = build_interventions(
        [
            {
                "id": "x",
                "intervention_type": "CarbonPriceShock",
                "target_ids": ["global"],
                "start_step": 0,
                "parameters": {"new_price_usd_per_tco2": 120},
            }
        ]
    )
    assert interventions[0].end_step is None


def test_build_intervention_unknown_type_raises_clear_error():
    spec = {
        "id": "x",
        "intervention_type": "NotRealIntervention",
        "target_ids": ["global"],
        "start_step": 0,
        "parameters": {},
    }
    with pytest.raises(ValueError) as exc_info:
        build_interventions([spec])
    msg = str(exc_info.value)
    assert "NotRealIntervention" in msg
    assert str(spec) in msg


def test_supply_disruption_missing_fuel_raises_intervention_error():
    intervention = FuelSupplyDisruption(
        id="d1",
        intervention_type="FuelSupplyDisruption",
        target_ids=["supplier_1"],
        start_step=0,
        parameters={"supplier_id": "supplier_1", "fuel_id": "green_hydrogen", "capacity_multiplier": 0.5},
    )
    with pytest.raises(InterventionError):
        intervention.apply(W([Supplier("supplier_1", {"green_methanol": 100.0})]), M())
