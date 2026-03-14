from __future__ import annotations

from .exceptions import ReportingError


def generate_report(run_result: dict) -> str:
    try:
        summary = run_result["summary"]
        events = run_result["events"]
        scenario = run_result["scenario"]
    except KeyError as exc:
        raise ReportingError(f"Missing report input field: {exc}") from exc

    if not isinstance(summary, dict):
        raise ReportingError("summary must be a mapping")

    fleet_share = summary.get("final_fleet_share_by_fuel")
    if not isinstance(fleet_share, dict) or not fleet_share:
        raise ReportingError("summary.final_fleet_share_by_fuel must be a non-empty mapping")

    try:
        cumulative_emissions = float(summary.get("cumulative_emissions", 0.0))
        cumulative_system_cost = float(summary.get("cumulative_system_cost", 0.0))
    except (TypeError, ValueError) as exc:
        raise ReportingError(f"Invalid numeric values in summary: {exc}") from exc

    try:
        top_share = max(fleet_share, key=fleet_share.get)
    except Exception as exc:
        raise ReportingError(f"Unable to determine top final fuel share: {exc}") from exc

    major_events = "\n".join([f"- step {e.get('step')}: {e.get('event_type')}" for e in events[:8]]) or "- none"

    return f"""# Renewable Fuel Twin Report

## 1. Executive Summary
Top final fuel: **{top_share}**. Cumulative emissions: **{cumulative_emissions:.2f}** tCO2e.

## 2. Scenario Description
Scenario: `{scenario}`.

## 3. Key Outcomes
- Final fleet share by fuel: {fleet_share}
- Cumulative system cost proxy: {cumulative_system_cost:.2f}

## 4. Why It Happened
Primary drivers: delivered cost differences, carbon price, and supply limits.

## 5. Timeline of Major Events
{major_events}

## 6. Sensitivity / Caveats
v1 simplified logistics and contracting assumptions.

## 7. Suggested Next Experiments
1. Increase carbon levy earlier.
2. Delay methanol support at a key port.
3. Add additional supplier reliability shocks.
"""
