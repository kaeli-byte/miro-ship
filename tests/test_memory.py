from renewable_fuel_twin.memory import AgentMemory


def test_memory_ops():
    mem = AgentMemory()
    mem.append_event({"event": 1})
    mem.update_beliefs({"x": 0.2})
    mem.record_plan("do")
    assert mem.summarize_recent(1)[0]["event"] == 1
    assert mem.retrieve_salient_context("x") == 0.2
    assert "do" in mem.strategic
