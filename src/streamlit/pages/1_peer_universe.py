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
    # st.write("Enter the name of a company to get information about it.")

    # Input field to enter the company name
    company_ticker = st.text_input("Enter Primary Ticker", "")
    if company_ticker != "":
        st.session_state["main_ticker"] = company_ticker

    # Button to fetch company information
    if st.button("Set Primary Ticker", key="start_key") or st.session_state["main_ticker"]!="":
        main_ticker = YahooExtractor(company_ticker)
        suggested_peers = main_ticker.get_recommended_symbols()
        if suggested_peers is not None:
            suggested_peers = ", ".join(suggested_peers)
            st.write("Suggested peers", suggested_peers)
        else:
            st.write("There are no suggested peers")

        # Create a list of peers
        peer_list = []


        number_of_peers = st.number_input('Number of Peers', step=1, min_value=1)

        st.write("Write the Peers here")
        cols = st.columns(number_of_peers)
        for i in range(number_of_peers):
            col = cols[i]
            peer=col.text_input(label="", value="", key=i)
            peer_list.append(peer)

        st.session_state["peer_list"] = peer_list

        if st.button("Add Peers", key="add_peers"):
            full_df = main_ticker.get_stats()
            full_df["ticker"] = company_ticker
            
            for peer in peer_list:
                ticker_df = YahooExtractor(peer).get_stats()
                ticker_df["ticker"] = peer

                full_df = pd.concat([full_df, ticker_df], ignore_index=True)

            st.session_state["data"] = full_df
            print(full_df)

if __name__ == "__main__":
    main()