import pandas as pd
import json
import os

# Load the validation Excel data
validation_path = "validation_scenario.xlsx"
validation_df = pd.read_excel(validation_path)

# Load the exported JSON config and simulate the calculator
from calculations import Scenario, FinancialInputs, TEACalculator
from models import TEAConfig

# Assume config file is available in the same directory (mocked or real)
config_path = "./configs/validation_scenario.json"
assert os.path.exists(config_path), f"Config file not found: {config_path}"

# Load config
config = TEAConfig.from_json(config_path)
scenario = Scenario(**config.scenario.to_dict())
financials = FinancialInputs(**config.financials.to_dict())
calc = TEACalculator(scenario, financials)

# Recalculate tool outputs
tool_values = {
    "Year": [f"Year {i+1}" for i in range(financials.years)],
    "Subscribers": calc.project_subscribers(),
    "Subscription Revenue (€)": [s * financials.subscription_fee for s in calc.project_subscribers()],
    "Pay-Per-Use Revenue (€)": [s * financials.pay_per_use_fee for s in calc.project_subscribers()],
    "Total Revenue (€)": calc.project_revenue(),
    "OPEX (€)": calc.project_opex(),
    "Profit (€)": calc.calculate_profit(),
    "Cumulative Cash Flow (€)": calc.calculate_cumulative_cash_flow()
}

tool_df = pd.DataFrame(tool_values)

# Merge and compare
merged_df = validation_df.merge(tool_df, on="Year", suffixes=('_expected', '_tool'))

# Define assertion logic
def validate_column(col):
    return all(abs(merged_df[f"{col}_expected"] - merged_df[f"{col}_tool"]) < 1e-2)

comparison_results = {
    col: validate_column(col)
    for col in ["Subscribers", "Subscription Revenue (€)", "Pay-Per-Use Revenue (€)",
                "Total Revenue (€)", "OPEX (€)", "Profit (€)", "Cumulative Cash Flow (€)"]
}

print("Validation Comparison Table:")
print(merged_df)

comparison_results
