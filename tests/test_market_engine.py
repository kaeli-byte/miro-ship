from renewable_fuel_twin.market_engine import delivered_cost


def test_delivered_cost():
    assert delivered_cost(1, 2, 3, 4, 5, 6) == 21
