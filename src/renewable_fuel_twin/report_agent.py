from __future__ import annotations

from .exceptions import ReportingError


def generate_report(run_result: dict) -> str:
    try:
        summary = run_result["summary"]
        events = run_result["events"]
        scenario = run_result["scenario"]
    except KeyError as exc:
        raise ReportingError(f"Missing report input field: {exc}") from exc

    major_events = "\n".join([f"- step {e['step']}: {e['event_type']}" for e in events[:8]]) or "- none"
    top_share = max(summary["final_fleet_share_by_fuel"], key=summary["final_fleet_share_by_fuel"].get)
    return f"""# Renewable Fuel Twin Report

## 1. Executive Summary
Top final fuel: **{top_share}**. Cumulative emissions: **{summary['cumulative_emissions']:.2f}** tCO2e.

## 2. Scenario Description
Scenario: `{scenario}`.

## 3. Key Outcomes
- Final fleet share by fuel: {summary['final_fleet_share_by_fuel']}
- Cumulative system cost proxy: {summary['cumulative_system_cost']:.2f}

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
