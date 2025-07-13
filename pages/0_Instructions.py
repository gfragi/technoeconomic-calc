# pages/0_Instructions.py
import streamlit as st

st.set_page_config(page_title="Instructions", layout="wide")
st.title("📝 Instructions: How to Use the TEA Tool")

st.markdown("""
### 1. Define a Scenario
- Go to **Create or Edit Scenario** in the sidebar.
- Set the number of years to simulate.
- Enter **financial inputs**:
  - Subscription fee (€/year)
  - Pay-per-use revenue (€/year)
  - CAPEX: One-time investment
  - OPEX: Ongoing yearly operational costs
- Set **growth assumptions**:
  - Subscriber growth rate
  - OPEX growth rate
  - Discount rate for NPV

### 2. Save & Export
- Give your scenario a name (no spaces).
- Click **Save Scenario** to store it as a `.json` file.

### 3. Compare Scenarios
- Go to **Compare Scenarios** in the sidebar.
- Select 2 or more saved scenarios.
- View comparison plots and financial summary metrics.

### 4. Download Results
- You can export metrics as CSV.
- Use the plots to analyze profitability, break-even timing, and reverse pricing trends.

---

### ℹ️ Notes
- All revenue values are assumed **annual per user**.
- All costs are **in euros (€)**.
- Discount Rate is used to compute **NPV** (Net Present Value).

""")
