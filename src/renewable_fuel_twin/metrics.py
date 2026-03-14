from __future__ import annotations

from pathlib import Path

import pandas as pd


def collect_step_metrics(step: int, transactions: list) -> dict:
    total = len(transactions) or 1
    fuel_counts: dict[str, int] = {}
    fuel_costs: dict[str, list[float]] = {}
    emissions = 0.0
    unmet = 0.0
    for tx in transactions:
        fuel_counts[tx.fuel_id] = fuel_counts.get(tx.fuel_id, 0) + 1
        fuel_costs.setdefault(tx.fuel_id, []).append(tx.delivered_cost)
        emissions += tx.emissions
        unmet += tx.unmet_demand
    return {
        "step": step,
        "fleet_share_by_fuel": {f: c / total for f, c in fuel_counts.items()},
        "total_emissions_tco2e": emissions,
        "average_delivered_cost_by_fuel": {f: sum(v) / len(v) for f, v in fuel_costs.items()},
        "unmet_fuel_demand_by_fuel": unmet,
        "operator_switch_count": 0,
        "green_contract_share": sum(c for f, c in fuel_counts.items() if f != "fossil_marine_fuel") / total,
    }


def summarize_run(step_metrics: list[dict]) -> dict:
    final = step_metrics[-1]
    cumulative_system_cost = 0.0
    for step in step_metrics:
        avg_costs = step.get("average_delivered_cost_by_fuel", {})
        fleet_share = step.get("fleet_share_by_fuel", {})
        weighted_step_cost = sum(avg_costs.get(fuel, 0.0) * fleet_share.get(fuel, 0.0) for fuel in avg_costs)
        cumulative_system_cost += weighted_step_cost

    return {
        "final_fleet_share_by_fuel": final["fleet_share_by_fuel"],
        "cumulative_emissions": sum(x["total_emissions_tco2e"] for x in step_metrics),
        "cumulative_system_cost": cumulative_system_cost,
        "average_abatement_cost": 0.0,
        "stranded_asset_proxy": 0.0,
        "policy_cost_effectiveness": 0.0,
    }


def serialize_metrics(step_metrics: list[dict], summary: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(step_metrics).to_csv(out_dir / "metrics_step.csv", index=False)
    pd.Series(summary).to_json(out_dir / "metrics_summary.json", indent=2)


def serialize_agent_snapshots(rows: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_dir / "agent_snapshots.csv", index=False)
