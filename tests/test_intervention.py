from renewable_fuel_twin.intervention import CarbonPriceShock


class M:
    carbon_price = 0


def test_carbon_shock():
    i = CarbonPriceShock(id="x", intervention_type="CarbonPriceShock", target_ids=["global"], start_step=0, end_step=1, parameters={"new_price_usd_per_tco2": 100})
    m = M()
    i.apply(None, m)
    assert m.carbon_price == 100
