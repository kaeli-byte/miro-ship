import pytest

from renewable_fuel_twin.exceptions import ReportingError
from renewable_fuel_twin.report_agent import generate_report


def test_report_contains_sections():
    report = generate_report(
        {
            "summary": {
                "final_fleet_share_by_fuel": {"f": 1.0},
                "cumulative_emissions": 1.0,
                "cumulative_system_cost": 2.0,
            },
            "events": [{"step": 1, "event_type": "CarbonPriceShock"}],
            "scenario": "s",
        }
    )
    assert "Executive Summary" in report
    assert "{'f': 1.0}" in report
    assert "Cumulative emissions" in report
    assert "Cumulative system cost" in report
    assert "Scenario: `s`" in report
    assert "Timeline of Major Events" in report


def test_report_invalid_summary_raises():
    with pytest.raises(ReportingError):
        generate_report({"events": [], "scenario": "s"})
