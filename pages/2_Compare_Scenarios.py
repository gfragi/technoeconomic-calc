# app.py

import os
import pandas as pd
import streamlit as st

from calculations import Scenario, FinancialInputs, TEACalculator
from models import TEAConfig
from plots import (
    plot_cash_flow,
    plot_reverse_pricing,
    plot_annual_profit,
    plot_annual_revenue,
    plot_capex_vs_cumulative_profit
)

import plotly.graph_objects as go

st.set_page_config(page_title="Techno-Economic Analysis", layout="wide")
st.title("📊 Compare Saved Scenarios")

# --- Load configs ---
config_dir = "configs"
config_files = [f for f in os.listdir(config_dir) if f.endswith(".json")]
selected_files = st.sidebar.multiselect("📂 Select Scenario Configs", config_files, default=[config_files[0]])

# --- Process selected scenarios ---
scenario_results = {}
tags = {}

for file in selected_files:
    config_path = os.path.join(config_dir, file)
    loaded = TEAConfig.from_json(config_path)
    scenario_config = loaded.scenario
    name = file.replace(".json", "")
    tag = f"{scenario_config.name} ({scenario_config.subscriber_growth_rate:.0f}% subs/yr)"
    tags[name] = tag
    scn = Scenario(**loaded.scenario.to_dict())
    fin = FinancialInputs(**loaded.financials.to_dict())
    calc = TEACalculator(scn, fin)

    years = fin.years
    year_labels = [f"Year {i+1}" for i in range(years)]

    subs = calc.project_subscribers()
    opex = calc.project_opex()
    result = {
        "years": year_labels,
        "subscribers": subs,
        "revenues": calc.project_revenue(),
        "opex": opex,
        "profit": calc.calculate_profit(),
        "cum_cash_flow": calc.calculate_cumulative_cash_flow(),
        "npv": calc.calculate_npv(),
        "roi": calc.calculate_roi(),
        "breakeven_year": calc.calculate_breakeven_year(),
        "reverse_fee": [o / max(s, 1) for o, s in zip(opex, subs)]
    }

    scenario_results[name] = result

# --- Plots ---
if scenario_results:
    any_result = next(iter(scenario_results.values()))
    year_labels = any_result["years"]

    st.subheader("📈 Cumulative Cash Flow Comparison")
    cum_flows = {name: res["cum_cash_flow"] for name, res in scenario_results.items()}
    st.plotly_chart(plot_cash_flow(year_labels, cum_flows), use_container_width=True)

    # --- Break-even Year Comparison ---
    st.subheader("📌 Break-even Year Comparison")

    fig = go.Figure()
    for name, res in scenario_results.items():
        breakeven = res["breakeven_year"]
        fig.add_trace(go.Bar(
            x=[name],
            y=[breakeven if breakeven != -1 else None],
            text=[f"{breakeven}" if breakeven != -1 else "Not Reached"],
            textposition="auto",
            name=name
        ))

    fig.update_layout(
        title="Break-even Year by Scenario",
        xaxis_title="Scenario",
        yaxis_title="Year",
        yaxis=dict(dtick=1),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📉 Reverse Pricing Comparison")
    fig = go.Figure()
    for name, res in scenario_results.items():
        fig.add_trace(go.Scatter(x=year_labels, y=res["reverse_fee"], mode="lines+markers", name=name))
    fig.update_layout(title="Reverse Pricing (€/subscriber)", xaxis_title="Year", yaxis_title="Required Fee")
    st.plotly_chart(fig, use_container_width=True)

    # --- Annual Trends ---
    st.subheader("📈 Total Revenue Comparison")
    total_revenues = {name: res["revenues"] for name, res in scenario_results.items()}
    st.plotly_chart(plot_annual_revenue(year_labels, total_revenues), use_container_width=True)

    st.subheader("📉 Annual Profit Comparison")
    profits = {name: res["profit"] for name, res in scenario_results.items()}
    st.plotly_chart(plot_annual_profit(year_labels, profits), use_container_width=True)


    # --- CAPEX vs Cumulative Profit ---
    st.subheader("📦 CAPEX vs Cumulative Profit")
    for name, res in scenario_results.items():
        capex = TEAConfig.from_json(os.path.join(config_dir, name + ".json")).financials.capex
        fig = plot_capex_vs_cumulative_profit(res["years"], res["cum_cash_flow"], capex, title=f"{name} – CAPEX vs Cumulative Profit")
        st.plotly_chart(fig, use_container_width=True)



    # --- Metrics Summary ---
    st.subheader("📋 Scenario Summary Metrics")
    metrics_df = pd.DataFrame({
        "Scenario File": list(scenario_results.keys()),
        "Description": [tags[name] for name in scenario_results.keys()],
        "NPV (€)": [r["npv"] for r in scenario_results.values()],
        "ROI": [r["roi"] for r in scenario_results.values()],
        "Break-even Year": [r["breakeven_year"] for r in scenario_results.values()],
    })
    st.dataframe(metrics_df.style.format({"NPV (€)": "{:,.2f}", "ROI": "{:.2f}"}), use_container_width=True)

    # --- Optional CSV export ---
    csv = metrics_df.to_csv(index=False)
    st.download_button("📥 Download Metrics as CSV", csv, file_name="scenario_metrics_summary.csv", mime="text/csv")

else:
    st.info("Please select at least one scenario to compare.")





