from __future__ import annotations

import json
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path

from .agents import ShipOperatorAgent
from .exceptions import SimulationStateError
from .intervention import build_interventions
from .market_engine import clear_market
from .memory import AgentMemory
from .metrics import collect_step_metrics, serialize_agent_snapshots, serialize_metrics, summarize_run
from .personas import make_persona
from .plotting import plot_metrics
from .report_agent import generate_report
from .scenario import apply_scenario
from .schemas import AppConfig, ScenarioConfig
from .world_builder import World


class FuelMarketModel:
    def __init__(self, world: World, config: AppConfig):
        self.world = world
        self.config = config
        self.step_id = 0
        self.carbon_price = config.carbon_price_usd_per_tco2
        self.events: list[dict] = []
        fuel_ids = [f.id for f in world.entities["fuels"]]
        self.operators = []
        for o in world.entities["operators"]:
            operator_seed = config.simulation.seed + sum(ord(ch) for ch in o.id)
            self.operators.append(
                ShipOperatorAgent(
                    id=o.id,
                    memory=AgentMemory(semantic={"demand": float(o.fleet_size * 4)}),
                    preferred_fuels=o.preferred_fuels,
                    persona=make_persona("cost_minimizer_operator", fuel_ids, seed=operator_seed),
                )
            )
        self.fuel_map = {f.id: f for f in world.entities["fuels"]}

    def step(self) -> list:
        txs = clear_market(
            operators=self.operators,
            fuels=self.fuel_map,
            suppliers=self.world.entities["suppliers"],
            carbon_price=self.carbon_price,
            transport_premium=self.config.transport_premium,
            port_fee=self.config.port_fee,
        )
        self.step_id += 1
        return txs


def _sanitize_run_name(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", name.replace("/", "_").replace("\\", "_"))
    safe = safe.strip("._") or "scenario"
    return safe[:48]


def run_scenario(world: World, app_config: AppConfig, scenario: ScenarioConfig, output_root: Path = Path("outputs/runs")) -> dict:
    runtime = apply_scenario(app_config.simulation.steps, scenario)
    model = FuelMarketModel(world, app_config)
    interventions = build_interventions(runtime.interventions)
    step_metrics = []

    for step in range(runtime.steps):
        for intervention in interventions:
            if intervention.active(step):
                intervention.apply(world, model)
                model.events.append({"step": step, "event_type": intervention.intervention_type, "id": intervention.id})

        txs = model.step()
        step_metrics.append(collect_step_metrics(step, txs))

    summary = summarize_run(step_metrics)
    safe_name = _sanitize_run_name(runtime.name)
    run_id = f"{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{safe_name}_{uuid.uuid4().hex[:8]}"
    run_dir = output_root / run_id
    try:
        run_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise SimulationStateError(f"run directory collision: {run_dir}") from exc

    latest_path = output_root / "latest"
    latest_path.unlink(missing_ok=True)
    latest_path.symlink_to(run_dir.name)

    serialize_metrics(step_metrics, summary, run_dir)
    serialize_agent_snapshots([{"id": o.id, "demand": o.memory.semantic["demand"]} for o in model.operators], run_dir)

    events_path = run_dir / "events.jsonl"
    events_path.write_text("\n".join(json.dumps(e) for e in model.events), encoding="utf-8")
    (run_dir / "world_snapshot.json").write_text(json.dumps({k: [x.model_dump() for x in v] for k, v in world.entities.items()}, indent=2), encoding="utf-8")
    (run_dir / "config_snapshot.yaml").write_text(f"scenario: {runtime.name}\nsteps: {runtime.steps}\n", encoding="utf-8")

    report = generate_report({"summary": summary, "events": model.events, "scenario": runtime.name})
    (run_dir / "report.md").write_text(report, encoding="utf-8")
    plot_metrics(run_dir / "metrics_step.csv", run_dir / "figures")

    return {"run_dir": run_dir, "summary": summary, "events": model.events, "scenario": runtime.name}
