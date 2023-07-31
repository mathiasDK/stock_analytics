import streamlit as st
from utils.simulation import MonteCarloSimulation
from utils.styling import PrimaryColors
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def create_fig(
    estimates, current: float = None, x_format: str = None, **kwargs
) -> go.Figure:
    """Creating a histogram figure based on the estimates and with a line for the current/base value. 
    This will create a graph of the distribution of the estimates.

    Args:
        estimates (np.ndarray): An array of estimated values.
        current (float, optional): The current/base value - used to plotting a line. Defaults to None.
        x_format (str, optional): The format of the x axis ticks - can be adjusted to "%" for % values.. Defaults to None.

    Returns:
        go.Figure: The graph.
    """
    fig = px.histogram(
        estimates,
        histnorm="probability density",
        color_discrete_sequence=[PrimaryColors.PURPLE.value],
        **kwargs,
    )
    if x_format is not None:
        fig.update_layout(xaxis=dict(tickformat="0%"))

    fig.update_layout(showlegend=False, yaxis=dict(visible=False))
    if current is not None:
        fig.add_vline(
            x=current,
            line_width=3,
            line_dash="dash",
            line_color=PrimaryColors.ORANGE.value,
            annotation_text="Current Value",
        )
    return fig


def get_denominator(number: float):
    """Creating a more simple version of the number, i.e. converting 5.634.923 to 5.6 (Millions)

    Args:
        number (float): The number to be simplified.

    Returns:
        float: The denominator.
        str: The text to write how the numbers have been reduced.
    """
    if number * 1.0 / 1e12 > 5:
        return 1e12, " (Trillions)"
    elif number * 1.0 / 1e9 > 5:
        return 1e9, " (Billions)"
    elif number * 1.0 / 1e6 > 5:
        return 1e6, " (Millions)"
    elif number * 1.0 / 1e3 > 5:
        return 1e3, " (Thousands)"
    else:
        return 1, ""


def valuation_overview(
    market_cap: float,
    periods: float,
    kpi_current: float = 0,
    key: str = "",
    wanted_cagr: float = 0.0,
):
    if kpi_current != 0:
        financial_current = market_cap * 1.0 / kpi_current
    else:
        financial_current = 0

    kpi_c1, kpi_c2 = st.columns(2)
    kpi_estimate = kpi_c1.number_input(
        "Estimated", key="kpi_estimate_" + key, value=round(kpi_current, 0), step=0.1
    )
    kpi_std = kpi_c2.number_input(
        "Std", key="kpi_std_" + key, value=round(kpi_current / 25, 1), step=0.1
    )

    denominator, denominator_str = get_denominator(financial_current)

    financial_c1, financial_c2 = st.columns(2)
    financial_estimate = (
        financial_c1.number_input(
            f"Estimated future financial{denominator_str}",
            key="financial_estimate_" + key,
            value=round(financial_current * 1.0 / denominator, 1),
            step=0.1,
        )
        * denominator
    )
    financial_std = (
        financial_c2.number_input(
            f"Standard deviation of future financial{denominator_str}",
            key="financial_std_" + key,
            value=round(financial_current * 1.0 / denominator / 25.0, 1),
            step=0.1,
        )
        * denominator
    )

    vals = {
        "kpi_current": kpi_current,
        "kpi_estimated": kpi_estimate,
        "kpi_std": kpi_std,
        "financial_current": financial_current,
        "financial_estimated": financial_estimate,
        "financial_std": financial_std,
    }

    sim = MonteCarloSimulation(**vals)

    # Figures
    estimated_kpi_fig = create_fig(
        sim.get_kpi_distribution(),
        kpi_current,
        title="Estimated KPI",
        labels={"value": "KPI"},
    )
    estimated_financial_fig = create_fig(
        sim.get_financial_distribution(),
        financial_current,
        title="Estimated Financials",
        labels={"value": "Financials"},
    )
    estimated_valuation_fig = create_fig(
        sim.get_valuation_distribution(),
        market_cap,
        title="Estimated Valuation",
        labels={"value": "Estimated Valuation"},
    )

    cagr = sim.get_valuation_cagr_distribution(periods=periods)
    estimated_cagr_fig = create_fig(
        cagr,
        current=wanted_cagr,
        x_format="0%",
        title="Estimated CAGR",
        labels={"value": "CAGR"},
    )

    fig_c11, fig_c12 = st.columns(2)
    fig_c11.plotly_chart(estimated_kpi_fig, use_container_width=True)
    fig_c12.plotly_chart(estimated_financial_fig, use_container_width=True)

    fig_c21, fig_c22 = st.columns(2)
    fig_c21.plotly_chart(estimated_valuation_fig, use_container_width=True)
    fig_c22.plotly_chart(estimated_cagr_fig, use_container_width=True)

    st.write(
        f"There are {str(round(np.mean(cagr>wanted_cagr)*100, 1))} % probability of you getting a better CAGR than your needs based on these estimates."
    )


def main():
    st.title("Valuation")
    st.markdown(
        """
        This page can be used to get an idea of what an estimated valuation of the stock could be.

        This is done by estimating the kpi and the financials X periods into the future and then providing a variance for the numbers.
        E.g. a future PE of 25 and future earnings of 2.000.000 would give an estimated future market cap of 50.000.000.
        Then a monte carlo simulation is done with 10.000 iterations to come up with a best guess of the valuation distribution based on your input.

        Note that this is by no means a recommendation, but merely a tool for you to take some informed decisions.
        """
    )
    print("")
    print("Starting valuation")
    primary_ticker_name = st.session_state["main_ticker"]
    full_df = st.session_state["data"]
    market_cap = full_df[
        (full_df["ticker"] == primary_ticker_name)
        & (full_df["metric"] == "quarterlyMarketCap")
        & (full_df["date"] == "2023-03-31")
    ]["value"].values[0]
    price_earnings_forward = full_df[
        (full_df["ticker"] == primary_ticker_name)
        & (full_df["metric"] == "quarterlyForwardPeRatio")
        & (full_df["date"] == "2023-03-31")
    ]["value"].values[0]
    price_book = full_df[
        (full_df["ticker"] == primary_ticker_name)
        & (full_df["metric"] == "quarterlyPbRatio")
        & (full_df["date"] == "2023-03-31")
    ]["value"].values[0]
    price_sales = full_df[
        (full_df["ticker"] == primary_ticker_name)
        & (full_df["metric"] == "quarterlyPsRatio")
        & (full_df["date"] == "2023-03-31")
    ]["value"].values[0]

    print("market cap: ", market_cap)
    print("pe: ", price_earnings_forward)

    periods = st.number_input(
        "How far into the future is your estimates?",
        min_value=1.0,
        max_value=10.0,
        step=0.25,
        key="periods",
    )
    wanted_cagr = (
        st.number_input(
            "What is the wanted CAGR you want on your investments (in %)?",
            min_value=0.0,
            step=0.25,
            key="cagr",
        )
        / 100.0
    )

    with st.expander("Price Earnings (Forward)", expanded=False):
        earnings = market_cap / price_earnings_forward
        st.markdown(
            f"""
            The current market is {market_cap}
            The current price earnings is {price_earnings_forward}
            The current earnings are {earnings}
            """
        )
        valuation_overview(
            market_cap=market_cap,
            periods=periods,
            kpi_current=price_earnings_forward,
            key="PE",
            wanted_cagr=wanted_cagr,
        )

    with st.expander("Price Sales", expanded=False):
        st.write("something")
        valuation_overview(
            market_cap=market_cap, periods=periods, kpi_current=price_sales, key="PS"
        )

    with st.expander("Price Book", expanded=False):
        st.write("something")
        valuation_overview(
            market_cap=market_cap, periods=periods, kpi_current=price_book, key="PB"
        )


if __name__ == "__main__":
    main()
