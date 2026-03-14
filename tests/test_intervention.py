import pytest

from renewable_fuel_twin.exceptions import InterventionError
from renewable_fuel_twin.intervention import (
    CarbonPriceShock,
    FuelSupplyDisruption,
    PortDelayIntervention,
    build_interventions,
)


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


class Port:
    def __init__(self, pid: str, supported_fuels: list[str]):
        self.id = pid
        self.supported_fuels = supported_fuels


class WWithPorts:
    def __init__(self, ports):
        self.entities = {"ports": ports}


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


def test_carbon_shock_revert_restores_original_value():
    i = CarbonPriceShock(id="x", intervention_type="CarbonPriceShock", target_ids=["global"], start_step=0, end_step=1, parameters={"new_price_usd_per_tco2": 100})
    m = M()
    m.carbon_price = 12

    i.apply(None, m)
    i.apply(None, m)

    assert m.carbon_price == 100

    i.revert(None, m)

    assert m.carbon_price == 12


def test_port_delay_revert_restores_supported_fuels_snapshot():
    intervention = PortDelayIntervention(
        id="p1",
        intervention_type="PortDelayIntervention",
        target_ids=["port_1"],
        start_step=0,
        parameters={"fuel_id": "green_methanol"},
    )
    port = Port("port_1", ["green_methanol", "ammonia"])
    world = WWithPorts([port])

    intervention.apply(world, M())
    intervention.apply(world, M())

    assert port.supported_fuels == ["ammonia"]

    intervention.revert(world, M())

    assert port.supported_fuels == ["green_methanol", "ammonia"]


def test_supply_disruption_revert_restores_original_capacity_after_multiple_applies():
    intervention = FuelSupplyDisruption(
        id="d1",
        intervention_type="FuelSupplyDisruption",
        target_ids=["supplier_1"],
        start_step=0,
        parameters={"supplier_id": "supplier_1", "fuel_id": "green_methanol", "capacity_multiplier": 0.5},
    )
    supplier = Supplier("supplier_1", {"green_methanol": 100.0})
    world = W([supplier])

    intervention.apply(world, M())
    intervention.apply(world, M())

    assert supplier.max_supply_by_fuel["green_methanol"] == 50.0

    intervention.revert(world, M())

    assert supplier.max_supply_by_fuel["green_methanol"] == 100.0
