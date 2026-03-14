from renewable_fuel_twin.market_engine import MarketTransaction
from renewable_fuel_twin.metrics import collect_step_metrics, summarize_run


def test_collect_metrics():
    m = collect_step_metrics(
        0,
        [
            MarketTransaction(
                operator_id="o",
                fuel_id="fossil_marine_fuel",
                delivered_cost=10,
                emissions=1,
                demand=100,
                unmet_demand=0,
            )
        ],
    )
    assert m["total_emissions_tco2e"] == 1


def test_summarize_run_weighted_cost():
    summary = summarize_run(
        [
            {
                "fleet_share_by_fuel": {"a": 0.25, "b": 0.75},
                "average_delivered_cost_by_fuel": {"a": 100.0, "b": 200.0},
                "total_emissions_tco2e": 1.0,
            }
        ]
    )
    assert summary["cumulative_system_cost"] == 175.0
