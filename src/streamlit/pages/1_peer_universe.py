import streamlit as st
from utils.yf_extractor import YahooExtractor
import pandas as pd


def main():
    # Set the title and description of the app
    st.title("Peer Universe")
    st.markdown(
        """
        Use this page to set the primary ticker and the peers you wish to see the KPIs for.
        """
    )

    # Input field to enter the company name
    company_ticker = st.text_input("Enter Primary Ticker", "")
    if company_ticker != "":
        st.session_state[
            "main_ticker"
        ] = company_ticker  # Making sure that the primary ticker is remembered until it is changed.

    # Button to fetch company information if there is a primary ticker
    if (
        st.button("Set Primary Ticker", key="start_key")
        or st.session_state["main_ticker"] != ""
    ):

        # The recommended symbols from Yahoo Finance (if any)
        main_ticker = YahooExtractor(company_ticker)
        suggested_peers = main_ticker.get_recommended_symbols()
        if suggested_peers is not None:
            suggested_peers = ", ".join(suggested_peers)
            st.write("Suggested peers", suggested_peers)
        else:
            st.write("There are no suggested peers")

        # Create a list of peers
        peer_list = []
        number_of_peers = st.number_input("Number of Peers", step=1, min_value=1)

        st.write("Write the Peers here")
        cols = st.columns(
            number_of_peers
        )  # Adapting according to how many peers one wish to include.
        for i in range(number_of_peers):
            col = cols[i]
            peer = col.text_input(label="", value="", key=i)
            peer_list.append(peer)

        st.session_state[
            "peer_list"
        ] = peer_list  # Remembering the list of peers for the analysis page.

        if st.button("Add Peers", key="add_peers"):
            full_df = main_ticker.get_stats()
            full_df["ticker"] = company_ticker

            # Adding a progress bar for loading the data
            progress_text = "Loading data from yahoo"
            yahoo_extract_progress = st.progress(
                0, text=progress_text
            )  # If users move too fast the data won't be stored.

            for i, peer in enumerate(peer_list):
                # Extracting data for each peer and adding it to the dataframe
                ticker_df = YahooExtractor(peer).get_stats()
                ticker_df["ticker"] = peer

                full_df = pd.concat([full_df, ticker_df], ignore_index=True)

                progress = (i + 1.0) / (
                    number_of_peers + 1.0
                )  # Adding one so the final step is when the data is stored
                yahoo_extract_progress.progress(progress, text=progress_text)

            st.session_state[
                "data"
            ] = full_df  # Storing the data for the analysis page.
            yahoo_extract_progress.progress(1.0, text="Done loading data")


if __name__ == "__main__":
    main()
