
from typing import List


def calculate_min_fee_per_user(
    projected_subscribers: List[int],
    opex_per_year: List[float],
    capex: float = 0.0,
    amortize_capex_years: int = 1,
    add_margin: float = 0.0,
) -> List[float]:
    """
    Calculate the minimum required fee per subscriber to cover OPEX (and optionally CAPEX).

    Args:
        projected_subscribers: List of subscriber numbers per year
        opex_per_year: List of annual OPEX values
        capex: Total CAPEX to spread across years (optional)
        amortize_capex_years: Number of years over which to amortize CAPEX
        add_margin: Optional % markup on top of breakeven fee (e.g., 0.1 for 10%)

    Returns:
        List of required fees (€ per user) for each year
    """
    amortized_capex = [capex / amortize_capex_years if i < amortize_capex_years else 0.0 for i in range(len(opex_per_year))]
    total_required = [o + c for o, c in zip(opex_per_year, amortized_capex)]

    required_fees = []
    for users, total_cost in zip(projected_subscribers, total_required):
        fee = total_cost / max(users, 1)
        fee *= (1 + add_margin)
        required_fees.append(fee)

    return required_fees
