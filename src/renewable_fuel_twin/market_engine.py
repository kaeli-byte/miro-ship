from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarketTransaction:
    operator_id: str
    fuel_id: str
    delivered_cost: float
    emissions: float
    demand: float
    unmet_demand: float


def delivered_cost(base_price: float, supplier_markup: float, transport_premium: float, carbon_cost: float, port_fee: float, disruption_risk_premium: float) -> float:
    return base_price + supplier_markup + transport_premium + carbon_cost + port_fee + disruption_risk_premium


def score_fuel(cost: float, infra_risk: float, op_risk: float, inertia: float, infra_bonus: float, tech_bonus: float, cargo_bonus: float) -> float:
    return -(cost + infra_risk + op_risk + inertia) + infra_bonus + tech_bonus + cargo_bonus


def clear_market(operators: list, fuels: dict, suppliers: list, carbon_price: float, transport_premium: float, port_fee: float) -> list[MarketTransaction]:
    transactions: list[MarketTransaction] = []
    supply = {}
    for supplier in suppliers:
        for fuel, cap in supplier.max_supply_by_fuel.items():
            supply[fuel] = supply.get(fuel, 0.0) + cap

    for operator in operators:
        options = {}
        for fuel_id in operator.preferred_fuels:
            fuel = fuels[fuel_id]
            cost = delivered_cost(
                fuel.base_price_usd_per_tonne,
                25,
                transport_premium,
                fuel.emission_factor_tco2e_per_tonne * carbon_price,
                port_fee,
                10,
            )
            options[fuel_id] = score_fuel(cost, 20 * (1 - fuel.infra_maturity_score), 20 * fuel.operational_risk_score, operator.persona.switching_inertia * 10, 5, 5, 5)

        demand = float(operator.memory.semantic.get("demand", 100.0))
        filtered_options = {fuel_id: score for fuel_id, score in options.items() if supply.get(fuel_id, 0.0) > 0.0}

        if not filtered_options:
            transactions.append(
                MarketTransaction(
                    operator_id=operator.id,
                    fuel_id="unallocated",
                    delivered_cost=0.0,
                    emissions=0.0,
                    demand=demand,
                    unmet_demand=demand,
                )
            )
            continue

        chosen = operator.choose_fuel(filtered_options)
        available = supply.get(chosen, 0.0)
        allocated = min(demand, available)
        supply[chosen] = max(0.0, available - allocated)
        fuel = fuels[chosen]
        tx_cost = delivered_cost(fuel.base_price_usd_per_tonne, 25, transport_premium, fuel.emission_factor_tco2e_per_tonne * carbon_price, port_fee, 10)
        transactions.append(
            MarketTransaction(
                operator_id=operator.id,
                fuel_id=chosen,
                delivered_cost=tx_cost,
                emissions=allocated * fuel.emission_factor_tco2e_per_tonne,
                demand=demand,
                unmet_demand=max(0.0, demand - allocated),
            )
        )
    return transactions
