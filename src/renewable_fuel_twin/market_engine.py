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
    """
    Compute the total delivered cost per tonne by summing all cost components.
    
    Parameters:
        base_price (float): Base commodity price in USD per tonne.
        supplier_markup (float): Supplier markup in USD per tonne.
        transport_premium (float): Transport premium in USD per tonne.
        carbon_cost (float): Carbon cost in USD per tonne.
        port_fee (float): Port fee in USD per tonne.
        disruption_risk_premium (float): Premium for disruption risk in USD per tonne.
    
    Returns:
        total_cost (float): Total delivered cost in USD per tonne.
    """
    return base_price + supplier_markup + transport_premium + carbon_cost + port_fee + disruption_risk_premium


def score_fuel(cost: float, infra_risk: float, op_risk: float, inertia: float, infra_bonus: float, tech_bonus: float, cargo_bonus: float) -> float:
    """
    Compute a numeric attractiveness score for a fuel option.
    
    Parameters:
        cost (float): Delivered cost contribution for the fuel.
        infra_risk (float): Infrastructure-related penalty.
        op_risk (float): Operational risk penalty.
        inertia (float): Operator switching inertia penalty.
        infra_bonus (float): Bonus for infrastructure maturity or availability.
        tech_bonus (float): Technical capability bonus.
        cargo_bonus (float): Cargo/logistics bonus.
    
    Returns:
        score (float): Combined score where higher values indicate a more attractive fuel option.
    """
    return -(cost + infra_risk + op_risk + inertia) + infra_bonus + tech_bonus + cargo_bonus


def clear_market(operators: list, fuels: dict, suppliers: list, carbon_price: float, transport_premium: float, port_fee: float) -> list[MarketTransaction]:
    """
    Simulate market clearing: allocate available fuel supply to operators and record resulting transactions.
    
    Aggregates total available supply per fuel from suppliers, lets each operator evaluate and choose among their preferred fuels, allocates up to each operator's demand from available supply, and records a MarketTransaction for each operator with delivered cost, emissions, demand, and unmet demand.
    
    Parameters:
        operators (list): Operator objects with attributes `id`, `preferred_fuels` (iterable of fuel ids), `choose_fuel(options)` (callable), `persona.switching_inertia` (numeric), and `memory.semantic` (dict, may contain `"demand"`).
        fuels (dict): Mapping from fuel id to fuel objects with attributes `base_price_usd_per_tonne`, `emission_factor_tco2e_per_tonne`, `infra_maturity_score`, and `operational_risk_score`.
        suppliers (list): Supplier objects exposing `max_supply_by_fuel` (mapping of fuel id to available capacity).
        carbon_price (float): Carbon cost per tCO2e used to compute carbon component of delivered cost.
        transport_premium (float): Transport premium added to delivered cost.
        port_fee (float): Port fee added to delivered cost.
    
    Returns:
        list[MarketTransaction]: One MarketTransaction per operator containing:
            - operator_id: the operator's id
            - fuel_id: chosen fuel id
            - delivered_cost: computed delivered cost for the transaction
            - emissions: allocated quantity multiplied by the fuel's emission factor (tCO2e)
            - demand: operator's requested demand
            - unmet_demand: demand minus allocated quantity (0 if fully met)
    """
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

        chosen = operator.choose_fuel(options)
        demand = float(operator.memory.semantic.get("demand", 100.0))
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
