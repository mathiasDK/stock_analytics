import streamlit as st


st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

# Setting states
st.session_state["main_ticker"] = ""
st.session_state["peer_list"] = []
st.session_state["data"] = None
for peer in range(1, 10):
    peer_idx = "peer" + str(peer)
    if peer_idx + "_name" not in st.session_state:
        st.session_state[peer_idx + "_visible"] = True
        st.session_state[peer_idx + "_name"] = ""


def main():
    st.title("Peer Universe")
    st.markdown(
        """
        Welcome to the Peer Universe app!

        The purpose of this app is to provide deeper insights into any particular stock of interest through the KPIs which are available on yahoo finance.
        This can be used to make estimated guesses about how the KPIs will variate, assuming that the best insight about a particular stock is given by its peers.
        It should be noted that this is will not by any means give a full picture of a stock and the investment case, but merely be a tool to place it among its peers.

        This can be used to say that it might not be unrealistic that a stock's PE goes from 15 to 25 within a certain timeframe, and then you still need to provide your
        own best guess of future earning to be able to say anything about the valuation in the future.

        How to use the tool:
        1. Set the primary ticker and its peers.
        2. Navigate to the analysis page and explore some of the KPIs to see how the stock of interest performs compared to its peers.

        Note that if you look at a metric that is not a ratio, then different currencies will naturally make the values different across the peers.
        """
    )


if __name__ == "__main__":
    main()
