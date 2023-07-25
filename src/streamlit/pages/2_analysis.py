import streamlit as st
from utils.plotter import Plotter
from utils.yf_extractor import YahooExtractor


def main():
    # Extracting data from previous page
    primary_ticker_name = st.session_state["main_ticker"]
    main_ticker = YahooExtractor(primary_ticker_name)
    peer_list = st.session_state["peer_list"]
    full_df = st.session_state["data"]

    st.write(f"The main ticker is {primary_ticker_name}")
    st.write(f"The peers are {', '.join(peer_list)}")

    # Creating visuals

    # Finding what metrics to show:
    total_tickers = len(peer_list) + 1
    ticker_limit = (
        total_tickers * 0.75
    )  # At least 75 % of the tickers must be represented in the metric before it is shown.
    metric_df = full_df.groupby(["metric"])["ticker"].nunique().reset_index()
    metrics = metric_df[metric_df["ticker"] >= ticker_limit]["metric"].tolist()

    # Seleting a metric and adapting the df to it
    chosen_metric = st.selectbox(label="Selected Metric", options=metrics)
    df = full_df[full_df["metric"] == chosen_metric].copy()
    df[chosen_metric] = df["value"]

    # Plotting
    p = Plotter(df, primary_ticker=primary_ticker_name, peers=peer_list)

    development_plot = p.line(y_col=chosen_metric)
    mask = (df["date"] == "2023-03-31").tolist()
    current_state_plot = p.bar(y_col=chosen_metric, mask=df["date"] == "2023-03-31")

    st.plotly_chart(current_state_plot)
    st.plotly_chart(development_plot)


def blocker():
    st.write(
        "You have to select a stock of interest and one or multiple peers to use this page."
    )
    st.write("Please navigate to the peer universe page.")


if __name__ == "__main__":
    if st.session_state["main_ticker"] == "":
        blocker()
    elif st.session_state["peer_list"][0] == "":
        blocker()
    else:
        main()
