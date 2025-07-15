
import plotly.graph_objects as go
from typing import List, Dict


def plot_revenue_breakdown(years: List[int], subscription_rev: List[float], pay_per_use_rev: List[float], title: str = "Revenue Breakdown"):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=subscription_rev, name="Subscription Revenue"))
    fig.add_trace(go.Bar(x=years, y=pay_per_use_rev, name="Pay-per-Use Revenue"))
    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis_title="Year",
        yaxis_title="Revenue (€)"
    )
    return fig


def plot_opex(years: List[int], opex: List[float], title: str = "OPEX Over Time"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=opex, mode='lines+markers', name="OPEX"))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="OPEX (€)"
    )
    return fig


def plot_cash_flow(years: List[int], cash_flows_by_scenario: Dict[str, List[float]], title: str = "Cumulative Cash Flow"):
    fig = go.Figure()
    for scenario_name, cash_flow in cash_flows_by_scenario.items():
        fig.add_trace(go.Scatter(x=years, y=cash_flow, mode='lines+markers', name=scenario_name))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Cumulative Cash Flow (€)"
    )
    return fig


def plot_breakeven(cumulative_cash_flow: List[float], years: List[int], title: str = "Breakeven Analysis"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=cumulative_cash_flow, mode='lines+markers', name="Cumulative Cash Flow"))

    # Mark breakeven point
    for i, val in enumerate(cumulative_cash_flow):
        if val >= 0:
            fig.add_trace(go.Scatter(
                x=[years[i]], y=[val],
                mode='markers+text',
                name="Break-even",
                marker=dict(size=12, color="red"),
                text=["Break-even"],
                textposition="top center"
            ))
            break

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Cumulative Cash Flow (€)",
        showlegend=True
    )
    return fig


def plot_reverse_pricing(years: List[int], required_fees: List[float], title: str = "Reverse Pricing Curve"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=required_fees, mode='lines+markers', name="Required Fee"))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="€ per Subscriber to Cover OPEX"
    )
    return fig


def plot_annual_profit(years: List[int], profit_by_scenario: Dict[str, List[float]], title: str = "Annual Profit Comparison"):
    fig = go.Figure()
    for scenario_name, profits in profit_by_scenario.items():
        fig.add_trace(go.Scatter(x=years, y=profits, mode='lines+markers', name=scenario_name))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Profit (€)"
    )
    return fig


def plot_annual_revenue(years: List[int], revenue_by_scenario: Dict[str, List[float]], title: str = "Total Revenue Comparison"):
    fig = go.Figure()
    for scenario_name, revenues in revenue_by_scenario.items():
        fig.add_trace(go.Scatter(x=years, y=revenues, mode='lines+markers', name=scenario_name))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Revenue (€)"
    )
    return fig


def plot_profit_margin(years: List[int], margin_by_scenario: Dict[str, List[float]], title: str = "Profit Margin Comparison"):
    fig = go.Figure()
    for scenario_name, margins in margin_by_scenario.items():
        fig.add_trace(go.Scatter(x=years, y=margins, mode='lines+markers', name=scenario_name))
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Profit Margin (%)"
    )
    return fig


def plot_capex_vs_cumulative_profit(years: List[str], cum_profit: List[float], capex: float, title: str = "CAPEX vs Cumulative Profit"):
    fig = go.Figure()

    # Bar for CAPEX (shown only at Year 0)
    fig.add_trace(go.Bar(
        x=[years[0]],
        y=[capex],
        name="CAPEX",
        marker_color="indianred"
    ))

    # Line for cumulative profit
    fig.add_trace(go.Scatter(
        x=years,
        y=cum_profit,
        mode="lines+markers",
        name="Cumulative Profit",
        line=dict(color="seagreen")
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="€",
        barmode='group'
    )
    return fig


def plot_user_model_split(year_labels, subscription_users, ppu_users):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=year_labels,
        y=subscription_users,
        name="Subscription Users",
    ))
    fig.add_trace(go.Bar(
        x=year_labels,
        y=ppu_users,
        name="Pay-per-Use Users",
    ))

    fig.update_layout(
        barmode="stack",
        title="📊 User Model Split Over Time",
        xaxis_title="Year",
        yaxis_title="Number of Users",
        legend=dict(x=0.01, y=0.99)
    )

    return fig