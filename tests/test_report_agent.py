from renewable_fuel_twin.report_agent import generate_report


def test_report_contains_sections():
    report = generate_report({"summary": {"final_fleet_share_by_fuel": {"f": 1.0}, "cumulative_emissions": 1.0, "cumulative_system_cost": 2.0}, "events": [], "scenario": "s"})
    assert "Executive Summary" in report
