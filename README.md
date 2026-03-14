# Renewable Fuel Twin

A clean, testable Python project for simulating renewable shipping fuel competition using a deterministic, seed-driven market twin.

## Purpose
Model market dynamics among green methanol, green ammonia, green hydrogen, and fossil marine fuel under policy, infrastructure, and supply interventions.

## Architecture
- **Config + schemas**: Pydantic-validated app, world, and scenario definitions.
- **Seed ingestion**: JSON/YAML/CSV parsing into typed entities.
- **World builder**: object model + NetworkX explainability graph.
- **Agents + personas + memory**: bounded-rational behavior support.
- **Market engine**: delivered cost and deterministic fuel choice/allocation.
- **Interventions + metrics + reporting**: auditable events and explainable outputs.

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quickstart
```bash
python scripts/build_world.py --seed-dir data/seeds --config configs/base.yaml
python scripts/run_simulation.py --scenario configs/scenario_baseline.yaml
python scripts/batch_run.py --scenarios \
  configs/scenario_baseline.yaml \
  configs/scenario_carbon_levy.yaml \
  configs/scenario_port_delay.yaml \
  configs/scenario_methanol_supply_shock.yaml
python scripts/generate_report.py --run-dir outputs/runs/<run_id>
```
`outputs/runs/latest` is a convenience symlink created by `run_simulation.py` / `batch_run.py`; you can pass that path instead of `<run_id>` when present.

## Scenarios
- `configs/scenario_baseline.yaml`
- `configs/scenario_carbon_levy.yaml`
- `configs/scenario_port_delay.yaml`
- `configs/scenario_methanol_supply_shock.yaml`

## Outputs
Runs are written under `outputs/runs/<run_id>/` including metrics, events, snapshots, and report markdown.

## Testing
```bash
pytest -q
```

## Extension guide
- Add schema field(s) in `schemas.py`
- Extend config in `config.py`
- Add market logic in `market_engine.py`
- Register new intervention in `intervention.py`
