from renewable_fuel_twin.intervention import CarbonPriceShock, build_interventions


class M:
    carbon_price = 0


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
    try:
        build_interventions([spec])
    except ValueError as exc:
        msg = str(exc)
        assert "NotRealIntervention" in msg
        assert str(spec) in msg
    else:
        raise AssertionError("Expected ValueError for unknown intervention type")
