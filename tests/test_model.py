from pathlib import Path

from renewable_fuel_twin.config import load_app_config, load_scenario_config
from renewable_fuel_twin.model import run_scenario
from renewable_fuel_twin.world_builder import build_world


def test_run_scenario(tmp_path):
    app_config = load_app_config(Path("configs/base.yaml"))
    world = build_world(Path("data/seeds"), app_config)
    result = run_scenario(world, app_config, load_scenario_config(Path("configs/scenario_baseline.yaml")), output_root=tmp_path)
    assert (result["run_dir"] / "report.md").exists()


def test_run_scenario_applies_and_reverts_on_activation_transitions(tmp_path, monkeypatch):
    from types import SimpleNamespace

    world = SimpleNamespace(entities={"fuels": [], "operators": [], "suppliers": []})
    app_config = SimpleNamespace(
        simulation=SimpleNamespace(steps=1, seed=1),
        carbon_price_usd_per_tco2=0.0,
        transport_premium=0.0,
        port_fee=0.0,
    )
    scenario = SimpleNamespace(name="transition_test", interventions=[])

    class DummyIntervention:
        def __init__(self):
            self.id = "i1"
            self.intervention_type = "Dummy"
            self.calls = []

        def active(self, step):
            return step == 1

        def apply(self, world, model):
            self.calls.append(("apply", model.step_id))

        def revert(self, world, model):
            self.calls.append(("revert", model.step_id))

    intervention = DummyIntervention()

    monkeypatch.setattr("renewable_fuel_twin.model.apply_scenario", lambda steps, scenario: SimpleNamespace(steps=3, interventions=[], name="transition_test"))
    monkeypatch.setattr("renewable_fuel_twin.model.build_interventions", lambda specs: [intervention])
    monkeypatch.setattr("renewable_fuel_twin.model.collect_step_metrics", lambda step, txs: {"step": step})
    monkeypatch.setattr("renewable_fuel_twin.model.summarize_run", lambda step_metrics: {"steps": len(step_metrics)})
    monkeypatch.setattr("renewable_fuel_twin.model.serialize_metrics", lambda *args, **kwargs: None)
    monkeypatch.setattr("renewable_fuel_twin.model.serialize_agent_snapshots", lambda *args, **kwargs: None)
    monkeypatch.setattr("renewable_fuel_twin.model.generate_report", lambda payload: "report")
    monkeypatch.setattr("renewable_fuel_twin.model.plot_metrics", lambda *args, **kwargs: None)

    result = run_scenario(world, app_config, scenario, output_root=tmp_path)

    assert result["events"] == [
        {"step": 1, "event_type": "Dummy", "id": "i1", "transition": "activated"},
        {"step": 2, "event_type": "Dummy", "id": "i1", "transition": "reverted"},
    ]
    assert intervention.calls == [("apply", 1), ("revert", 2)]
