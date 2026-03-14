from renewable_fuel_twin.market_engine import MarketTransaction
from renewable_fuel_twin.metrics import collect_step_metrics


def test_collect_metrics():
    m = collect_step_metrics(0, [MarketTransaction("o", "fossil_marine_fuel", 10, 1, 100, 0)])
    assert m["total_emissions_tco2e"] == 1
