
from typing import Dict, List, Tuple
import numpy as np

class Scenario:
    def __init__(self, name: str, subscriber_growth_rate: float, opex_growth_rate: float, discount_rate: float):
        self.name = name
        self.subscriber_growth_rate = subscriber_growth_rate / 100
        self.opex_growth_rate = opex_growth_rate / 100
        self.discount_rate = discount_rate / 100

class FinancialInputs:
    def __init__(self,
                 starting_subscribers: int,
                 subscription_fee: float,
                 pay_per_use_fee: float,
                 base_opex: float,
                 capex: float = 0.0,
                 years: int = 5,
                 subscription_ratio: float = 1.0 ):
        self.starting_subscribers = starting_subscribers
        self.subscription_fee = subscription_fee
        self.pay_per_use_fee = pay_per_use_fee
        self.base_opex = base_opex
        self.capex = capex
        self.years = years
        self.subscription_ratio = subscription_ratio  # 0.0 to 1.0

class TEACalculator:

    def __init__(self, scenario: Scenario, inputs: FinancialInputs):
        self.scenario = scenario
        self.inputs = inputs

    def project_subscribers(self) -> List[int]:
        subs = [self.inputs.starting_subscribers]
        for _ in range(1, self.inputs.years):
            subs.append(subs[-1] * (1 + self.scenario.subscriber_growth_rate))
        return [int(s) for s in subs]

    def project_opex(self) -> List[float]:
        opex = [self.inputs.base_opex]
        for _ in range(1, self.inputs.years):
            opex.append(opex[-1] * (1 + self.scenario.opex_growth_rate))
        return opex

    def project_revenue(self) -> List[float]:
        subscribers = self.project_subscribers()
        r_sub = self.inputs.subscription_ratio
        r_ppu = 1 - r_sub

        revenue = []
        for s in subscribers:
            s_sub = s * r_sub
            s_ppu = s * r_ppu
            total = (s_sub * self.inputs.subscription_fee) + (s_ppu * self.inputs.pay_per_use_fee)
            revenue.append(total)
        return revenue

    def project_revenue_breakdown(self) -> Tuple[List[float], List[float]]:
        subscribers = self.project_subscribers()
        r_sub = self.inputs.subscription_ratio
        r_ppu = 1 - r_sub

        rev_sub = []
        rev_ppu = []
        for s in subscribers:
            s_sub = s * r_sub
            s_ppu = s * r_ppu
            rev_sub.append(s_sub * self.inputs.subscription_fee)
            rev_ppu.append(s_ppu * self.inputs.pay_per_use_fee)

        return rev_sub, rev_ppu

    def calculate_profit(self) -> List[float]:
        revenue = self.project_revenue()
        opex = self.project_opex()
        return [r - o for r, o in zip(revenue, opex)]

    def calculate_cumulative_cash_flow(self) -> List[float]:
        profit = self.calculate_profit()
        capex = self.inputs.capex
        cum_cf = []
        total = -capex
        for p in profit:
            total += p
            cum_cf.append(total)
        return cum_cf

    def calculate_npv(self) -> float:
        profit = self.calculate_profit()
        dr = self.scenario.discount_rate
        return sum([p / ((1 + dr) ** (i+1)) for i, p in enumerate(profit)])

    def calculate_roi(self) -> float:
        total_profit = sum(self.calculate_profit())
        return (total_profit - self.inputs.capex) / self.inputs.capex if self.inputs.capex > 0 else float('inf')

    def calculate_breakeven_year(self) -> int:
        cashflow = self.calculate_cumulative_cash_flow()
        for i, cf in enumerate(cashflow):
            if cf >= 0:
                return i + 1
        return -1  # No breakeven within given years

