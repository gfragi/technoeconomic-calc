import os
import streamlit as st
from calculations import Scenario, FinancialInputs, TEACalculator
from models import TEAConfig, ScenarioConfig, FinancialInputsConfig
import pandas as pd

from plots import (
    plot_revenue_breakdown,
    plot_opex,
    plot_cash_flow,
    plot_breakeven,
    plot_reverse_pricing,
    plot_annual_profit,
    plot_annual_revenue
)
st.set_page_config(page_title="Techno-Economic Analysis", layout="wide")

# Load available config files
config_dir = "./configs"
config_files = [f for f in os.listdir(config_dir) if f.endswith(".json")]
selected_file = st.sidebar.selectbox("📂 Load Scenario Config", config_files)
# if st.session_state.get("last_config") != selected_file:
#     st.session_state["last_config"] = selected_file
#     st.experimental_rerun()

# Load selected config
config_path = os.path.join(config_dir, selected_file) if selected_file else None
loaded_config = TEAConfig.from_json(config_path)
scenario = Scenario(**loaded_config.scenario.to_dict())
inputs = FinancialInputs(**loaded_config.financials.to_dict())



st.title("📊 Techno-Economic Analysis Tool")

with st.expander("ℹ️ What do these values mean?"):
    st.markdown("""
    - **CAPEX**: One-time capital expense in Year 0 (e.g., infrastructure setup).
    - **OPEX**: Ongoing yearly costs (e.g., salaries, licenses).
    - **Subscription & Pay-per-use fees**: Revenues per user per year.
    - **Reverse Pricing**: Minimum fee needed to break even, assuming subscriber projections hold.
    - All metrics are calculated **annually** and projected over the selected duration.
    """)



# --- Sidebar ---
st.sidebar.header("📥 Input Parameters")
st.sidebar.markdown("**ℹ️ All values are annual unless stated otherwise.**")

# After loading the config
fin = loaded_config.financials
scn = loaded_config.scenario

# Now use those variables safely
years = st.sidebar.slider("Years to project", 3, 10, value=fin.years, key="years", help="The number of years to include in the projection.")


starting_subs = st.sidebar.number_input("📦 Starting Subscribers (Year 0)", value=fin.starting_subscribers, key="subs")
sub_fee = st.sidebar.number_input("💶 Subscription Fee (€ / subscriber / year)", value=fin.subscription_fee, key="sub_fee")
ppu_fee = st.sidebar.number_input("💶 Pay-per-use Revenue (€ / subscriber /year)", value=fin.pay_per_use_fee, key="ppu_fee")
subscription_ratio = st.sidebar.slider(
    "🧮 % of Subscribers on Subscription Model",
    0, 100, int(getattr(fin, "subscription_ratio", 100)), step=5, key="sub_ratio",
    help="What percentage of users are charged via subscription vs. pay-per-use."
)
capex = st.sidebar.number_input("🏗️ CAPEX (one-time investment, €)", value=fin.capex, key="capex")
base_opex = st.sidebar.number_input("💸 Base OPEX (€ / year)", value=fin.base_opex, key="opex")

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Growth & Financial Assumptions")

sub_growth = st.sidebar.slider(
    "Subscriber Growth Rate (%)", 0.0, 50.0,
    float(scn.subscriber_growth_rate), step=0.1, key="sub_growth",
    help="Annual % growth in subscriber count."
)
opex_growth = st.sidebar.slider(
    "OPEX Growth Rate (%)", 0.0, 20.0,
    float(scn.opex_growth_rate), step=0.1, key="opex_growth",
    help="Annual % increase in operating expenses."
)
discount = st.sidebar.slider(
    "Discount Rate (%)", 0.0, 15.0,
    float(scn.discount_rate), step=0.1, key="discount",
    help="Used for NPV calculation (e.g., cost of capital)."
)


# --- Compute Scenario ---
scenario = Scenario("Base", subscriber_growth_rate=sub_growth, opex_growth_rate=opex_growth, discount_rate=discount)
inputs = FinancialInputs(
    starting_subscribers=starting_subs,
    subscription_fee=sub_fee,
    pay_per_use_fee=ppu_fee,
    base_opex=base_opex,
    capex=capex,
    years=years,
    subscription_ratio=subscription_ratio / 100.0  # convert to 0.0–1.0
)
calc = TEACalculator(scenario, inputs)

# --- Time Axis ---
year_labels = [f"Year {i+1}" for i in range(years)]

# --- Financial Calculations ---
subscribers = calc.project_subscribers()
subscription_users = [int(s * inputs.subscription_ratio) for s in subscribers]
ppu_users = [s - sub for s, sub in zip(subscribers, subscription_users)]

subscription_revenue = [n * sub_fee for n in subscription_users]
ppu_revenue = [n * ppu_fee for n in ppu_users]

revenues = [s + p for s, p in zip(subscription_revenue, ppu_revenue)]
opex = calc.project_opex()
profit = calc.calculate_profit()
cum_cash_flow = calc.calculate_cumulative_cash_flow()
npv = calc.calculate_npv()
roi = calc.calculate_roi()
breakeven_year = calc.calculate_breakeven_year()


# --- Layout ---
st.subheader("📈 Financial Projections")

col1, col2, col3 = st.columns(3)
col1.metric("NPV (€)", f"{npv:,.2f} €")
col2.metric("ROI (%)", f"{roi * 100:.1f} %" if roi != float('inf') else "∞")
col3.metric("Break-even Year", breakeven_year if breakeven_year != -1 else "Not Reached")

st.plotly_chart(plot_revenue_breakdown(year_labels, subscription_revenue, ppu_revenue), use_container_width=True)
st.plotly_chart(plot_opex(year_labels, opex), use_container_width=True)
st.plotly_chart(plot_cash_flow(year_labels, {"Base": cum_cash_flow}), use_container_width=True)
st.plotly_chart(plot_breakeven(cum_cash_flow, year_labels), use_container_width=True)

# --- Reverse Pricing ---
reverse_fees = [o / max(s, 1) for o, s in zip(opex, subscribers)]
st.plotly_chart(plot_reverse_pricing(year_labels, reverse_fees), use_container_width=True)

# --- Data Table View ---
st.subheader("📋 Financial Projection Table (Annual)")

subscription_users = [int(s * inputs.subscription_ratio) for s in subscribers]
ppu_users = [s - sub for s, sub in zip(subscribers, subscription_users)]

df = pd.DataFrame({
    "Year": year_labels,
    "Total Subscribers (users)": subscribers,
    "Subscription Model Users": subscription_users,
    "Pay-per-Use Model Users": ppu_users,
    "Subscription Revenue (€ / year)": subscription_revenue,
    "Pay-per-Use Revenue (€ / year)": ppu_revenue,
    "Total Revenue (€ / year)": revenues,
    "OPEX (€ / year)": opex,
    "Profit (€ / year)": profit,
    "Cumulative Cash Flow (€)": cum_cash_flow,
    "Reverse Pricing Fee (€ / user / year)": reverse_fees
})

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
st.dataframe(df.style.format({col: "{:,.2f}" for col in numeric_cols}), use_container_width=True)


st.sidebar.markdown("---")
st.sidebar.subheader("💾 Export New Scenario")

with st.sidebar.form("save_config_form"):
    new_config_name = st.text_input("Config Name (no spaces)", value="custom_config")
    save_it = st.form_submit_button("Save Scenario")

    if save_it and new_config_name:
        export_config = TEAConfig(
            scenario=ScenarioConfig(
                name=scenario.name,
                subscriber_growth_rate=scenario.subscriber_growth_rate * 100,
                opex_growth_rate=scenario.opex_growth_rate * 100,
                discount_rate=scenario.discount_rate * 100
            ),
            financials=FinancialInputsConfig(
                starting_subscribers=inputs.starting_subscribers,
                subscription_fee=inputs.subscription_fee,
                pay_per_use_fee=inputs.pay_per_use_fee,
                base_opex=inputs.base_opex,
                capex=inputs.capex,
                years=inputs.years
            )
        )
        save_path = os.path.join("configs", f"{new_config_name}.json")
        export_config.to_json(save_path)
        st.success(f"Saved as {save_path}")




# --- Optional Export ---
st.download_button("Download CSV", df.to_csv(index=False), file_name="techno_economic_projection.csv", mime="text/csv")
