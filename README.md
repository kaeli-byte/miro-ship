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
python scripts/batch_run.py --scenarios configs/scenario_baseline.yaml configs/scenario_carbon_levy.yaml
python scripts/generate_report.py --run-dir outputs/runs/latest
```

## Scenarios
- Baseline
- Strong carbon levy
- Port delay
- Methanol supply shock

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
