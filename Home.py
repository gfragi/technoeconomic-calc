# pages/0_Instructions.py
import streamlit as st

st.set_page_config(page_title="Instructions", layout="wide")
st.title("🧭 How to Use the Techno-Economic Analysis Tool")
st.caption("This guide helps you define, save, and compare business scenarios.")

# Step 1
st.header("📌 Step 1: Create a New Scenario")
st.markdown("""
Navigate to the **Create or Edit Scenario** page:

🔧 Set your scenario assumptions:
- **Years to Project**: 3–10 years
- **Starting Subscribers** (e.g., 20)
- **Subscription Fee** *(€/user/year)*
- **Pay-per-use Revenue** *(€/user/year)*
- **CAPEX** *(€ one-time investment)*
- **Base OPEX** *(€ per year)*

📈 Set your growth parameters:
- Subscriber Growth Rate *(% per year)*
- OPEX Growth Rate *(% per year)*
- Discount Rate *(% for NPV)*

💾 Click **Save Scenario** to export your config.
""")

# Divider
st.divider()

# Step 2
st.header("📊 Step 2: Compare Scenarios")
st.markdown("""
Go to the **Compare Scenarios** page:

📂 Select 2–3 saved scenarios from the sidebar.

🔍 Analyze:
- **Cumulative Cash Flow**
- **Reverse Pricing per Subscriber**
- **Annual Revenue or Profit**
- **Break-even timing**
- Scenario summary metrics (NPV, ROI, Break-even Year)

📥 You can also export a **CSV report** with the metrics.
""")

# Divider
st.divider()

# Step 3
st.header("💡 Example Use Cases")
st.markdown("""
This tool is designed to support:
- **Data Space Operators** assessing subscription/pay-per-use models
- **SaaS or cloud platform services** evaluating ROI & growth strategy
- **Startup planning** for CAPEX recovery and profitability analysis

📘 All values are **per year** unless otherwise specified.  
💶 All currency values are **in euros (€)**.
""")

# Footer
st.divider()
st.info("Need more help? Contact the project team or check the README file.")

