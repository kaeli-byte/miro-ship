from renewable_fuel_twin.personas import make_persona


def test_persona_deterministic():
    p1 = make_persona("cost_minimizer_operator", ["a"], seed=2)
    p2 = make_persona("cost_minimizer_operator", ["a"], seed=2)
    assert p1 == p2
