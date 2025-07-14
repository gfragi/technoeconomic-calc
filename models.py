
from dataclasses import dataclass, asdict
from typing import Dict, Any
import json


@dataclass
class ScenarioConfig:
    name: str
    subscriber_growth_rate: float
    opex_growth_rate: float
    discount_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return ScenarioConfig(**data)


@dataclass
class FinancialInputsConfig:
    starting_subscribers: int
    subscription_fee: float
    pay_per_use_fee: float
    base_opex: float
    capex: float
    years: int
    subscription_ratio: float = 1.0  # Default to 100% subscription
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return FinancialInputsConfig(**data)


@dataclass
class TEAConfig:
    scenario: ScenarioConfig
    financials: FinancialInputsConfig

    def to_json(self, path: str):
        with open(path, "w") as f:
            json.dump({
                "scenario": self.scenario.to_dict(),
                "financials": self.financials.to_dict()
            }, f, indent=2)

    @staticmethod
    def from_json(path: str):
        with open(path, "r") as f:
            data = json.load(f)
        scenario = ScenarioConfig.from_dict(data["scenario"])
        financials = FinancialInputsConfig.from_dict(data["financials"])
        return TEAConfig(scenario, financials)
