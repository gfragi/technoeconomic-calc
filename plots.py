
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
