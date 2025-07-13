import os
import streamlit as st
from calculations import Scenario, FinancialInputs, TEACalculator
from models import TEAConfig, ScenarioConfig, FinancialInputsConfig

from plots import (
    plot_revenue_breakdown,
    plot_opex,
    plot_cash_flow,
    plot_breakeven,
    plot_reverse_pricing
)
st.set_page_config(page_title="Techno-Economic Analysis", layout="wide")

# Load available config files
config_dir = "configs"
config_files = [f for f in os.listdir(config_dir) if f.endswith(".json")]
selected_file = st.sidebar.selectbox("📂 Load Scenario Config", config_files)

# Load selected config
config_path = os.path.join(config_dir, selected_file)
loaded_config = TEAConfig.from_json(config_path)
scenario = Scenario(**loaded_config.scenario.to_dict())
inputs = FinancialInputs(**loaded_config.financials.to_dict())



st.title("📊 Techno-Economic Analysis Tool")

# --- Sidebar Inputs ---
st.sidebar.header("📥 Input Parameters")

years = st.sidebar.slider("Years to project", 3, 10, 5)
starting_subs = st.sidebar.number_input("Starting Subscribers", value=100)
sub_fee = st.sidebar.number_input("Subscription Fee (€)", value=100.0)
ppu_fee = st.sidebar.number_input("Pay-per-use Fee (€)", value=20.0)
capex = st.sidebar.number_input("CAPEX (€)", value=30000.0)
base_opex = st.sidebar.number_input("Base OPEX (€)", value=10000.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Growth & Discount Assumptions")
sub_growth = st.sidebar.slider("Subscriber Growth Rate (%)", 0.0, 50.0, 20.0)
opex_growth = st.sidebar.slider("OPEX Growth Rate (%)", 0.0, 20.0, 10.0)
discount = st.sidebar.slider("Discount Rate (%)", 0.0, 15.0, 5.0)

# --- Compute Scenario ---
scenario = Scenario("Base", subscriber_growth_rate=sub_growth, opex_growth_rate=opex_growth, discount_rate=discount)
inputs = FinancialInputs(
    starting_subscribers=starting_subs,
    subscription_fee=sub_fee,
    pay_per_use_fee=ppu_fee,
    base_opex=base_opex,
    capex=capex,
    years=years
)
calc = TEACalculator(scenario, inputs)

# --- Time Axis ---
year_labels = [f"Year {i+1}" for i in range(years)]

# --- Financial Calculations ---
subscribers = calc.project_subscribers()
revenues = calc.project_revenue()
opex = calc.project_opex()
profit = calc.calculate_profit()
cum_cash_flow = calc.calculate_cumulative_cash_flow()
npv = calc.calculate_npv()
roi = calc.calculate_roi()
breakeven_year = calc.calculate_breakeven_year()

subscription_revenue = [s * sub_fee for s in subscribers]
ppu_revenue = [s * ppu_fee for s in subscribers]

# --- Layout ---
st.subheader("📈 Financial Projections")

col1, col2, col3 = st.columns(3)
col1.metric("NPV (€)", f"{npv:,.2f}")
col2.metric("ROI", f"{roi:.2f}" if roi != float('inf') else "∞")
col3.metric("Break-even Year", breakeven_year if breakeven_year != -1 else "Not Reached")

st.plotly_chart(plot_revenue_breakdown(year_labels, subscription_revenue, ppu_revenue), use_container_width=True)
st.plotly_chart(plot_opex(year_labels, opex), use_container_width=True)
st.plotly_chart(plot_cash_flow(year_labels, {"Base": cum_cash_flow}), use_container_width=True)
st.plotly_chart(plot_breakeven(cum_cash_flow, year_labels), use_container_width=True)

# --- Reverse Pricing ---
reverse_fees = [o / max(s, 1) for o, s in zip(opex, subscribers)]
st.plotly_chart(plot_reverse_pricing(year_labels, reverse_fees), use_container_width=True)

# --- Data Table View ---
st.subheader("📋 Raw Data Table")
import pandas as pd

df = pd.DataFrame({
    "Year": year_labels,
    "Subscribers": subscribers,
    "Subscription Revenue (€)": subscription_revenue,
    "Pay-per-Use Revenue (€)": ppu_revenue,
    "Total Revenue (€)": revenues,
    "OPEX (€)": opex,
    "Profit (€)": profit,
    "Cumulative Cash Flow (€)": cum_cash_flow,
    "Reverse Pricing Fee (€)": reverse_fees
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
