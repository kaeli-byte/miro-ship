from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pandas as pd


def collect_step_metrics(step: int, transactions: list) -> dict:
    """
    Aggregate per-step fleet, cost, emissions, and demand metrics from a list of transaction records.
    
    Parameters:
        step (int): The simulation step index for which metrics are computed.
        transactions (list): Iterable of transaction objects; each must provide
            attributes `fuel_id`, `delivered_cost`, `emissions`, and `unmet_demand`.
    
    Returns:
        dict: A dictionary containing:
            - "step": the provided step value.
            - "fleet_share_by_fuel": mapping of fuel_id to fraction of total transactions.
            - "total_emissions_tco2e": sum of `emissions` across transactions.
            - "average_delivered_cost_by_fuel": mapping of fuel_id to average `delivered_cost`.
            - "unmet_fuel_demand_by_fuel": total `unmet_demand` summed across transactions.
            - "operator_switch_count": integer placeholder (currently 0).
            - "green_contract_share": fraction of transactions not using "fossil_marine_fuel".
    """
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
    """
    Produce a run-level summary from a list of per-step metric dictionaries.
    
    Parameters:
        step_metrics (list[dict]): Ordered list of per-step metric dictionaries (as produced by collect_step_metrics), at least one element.
    
    Returns:
        dict: Summary containing:
            final_fleet_share_by_fuel (dict): fleet share by fuel from the final step.
            cumulative_emissions (float): sum of `total_emissions_tco2e` across all steps.
            cumulative_system_cost (float): sum across steps of the per-step sums of `average_delivered_cost_by_fuel`.
            average_abatement_cost (float): placeholder value (0.0).
            stranded_asset_proxy (float): placeholder value (0.0).
            policy_cost_effectiveness (float): placeholder value (0.0).
    """
    final = step_metrics[-1]
    return {
        "final_fleet_share_by_fuel": final["fleet_share_by_fuel"],
        "cumulative_emissions": sum(x["total_emissions_tco2e"] for x in step_metrics),
        "cumulative_system_cost": sum(sum(x["average_delivered_cost_by_fuel"].values()) for x in step_metrics),
        "average_abatement_cost": 0.0,
        "stranded_asset_proxy": 0.0,
        "policy_cost_effectiveness": 0.0,
    }


def serialize_metrics(step_metrics: list[dict], summary: dict, out_dir: Path) -> None:
    """
    Persist per-step metrics and a run summary to files in the specified output directory.
    
    Writes two files into out_dir:
    - metrics_step.csv: CSV representation of the provided list of per-step metric dictionaries.
    - metrics_summary.json: JSON representation of the summary dictionary (indented with 2 spaces).
    
    Parameters:
        step_metrics (list[dict]): Sequence of per-step metric dictionaries to serialize (each dictionary becomes a row in the CSV).
        summary (dict): Aggregated run summary to serialize as JSON.
        out_dir (Path): Target directory where the files will be created; the directory will be created if it does not exist.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(step_metrics).to_csv(out_dir / "metrics_step.csv", index=False)
    pd.Series(summary).to_json(out_dir / "metrics_summary.json", indent=2)


def serialize_agent_snapshots(rows: list[dict], out_dir: Path) -> None:
    """
    Persist a list of agent snapshot records to a CSV file named "agent_snapshots.csv" inside the given output directory.
    
    Parameters:
        rows (list[dict]): Sequence of mappings where each dict represents a single agent snapshot (keys become CSV columns).
        out_dir (Path): Destination directory for the output CSV file; the file will be written to `out_dir / "agent_snapshots.csv"`.
    """
    pd.DataFrame(rows).to_csv(out_dir / "agent_snapshots.csv", index=False)
