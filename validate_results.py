import json
import pandas as pd
import os

# --- Load reference CSV ---
csv_path = "./scenario_metrics_summary.csv"
reference_df = pd.read_csv(csv_path)

# --- Load JSON exports (your tool's outputs) ---
results_dir = "configs"
json_files = [f for f in os.listdir(results_dir) if f.endswith(".json")]

# --- Tolerance for floating point comparison ---
TOL = 1e-2

# --- Validate each scenario ---
for file in json_files:
    with open(os.path.join(results_dir, file)) as f:
        tool_output = json.load(f)
    
    name = file.replace(".json", "")
    print(f"🔍 Validating {name}...")

    if name not in reference_df["Scenario"].values:
        print(f"⚠️ Scenario '{name}' not found in CSV.")
        continue

    ref_row = reference_df[reference_df["Scenario"] == name].iloc[0]

    # Example metrics
    for field in ["NPV (€)", "ROI", "Break-even Year"]:
        tool_value = tool_output.get("metrics", {}).get(field)
        expected = ref_row[field]

        if pd.isna(expected):
            print(f"  ⚠️ {field}: Expected value missing.")
            continue

        # Compare with tolerance for floats
        if abs(float(tool_value) - float(expected)) > TOL:
            print(f"  ❌ {field} mismatch: Expected {expected}, got {tool_value}")
        else:
            print(f"  ✅ {field} OK")

print("✅ Validation complete.")
