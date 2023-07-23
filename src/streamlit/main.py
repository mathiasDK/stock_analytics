import streamlit as st


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# Setting states
st.session_state["main_ticker"] = ""
st.session_state["peer_list"] = []
st.session_state["data"] = None
for peer in range(1,10):
    peer_idx = "peer"+str(peer)
    if peer_idx+"_name" not in st.session_state:
        st.session_state[peer_idx+"_visible"] = True
        st.session_state[peer_idx+"_name"] = ""

def main():
    st.title("Peer Universe")
    st.markdown(
        """
        Welcome to the Peer Universe app!

        Approach:
        1. Set the primary ticker and its peers.
        2. Navigate to the analysis page and explore some of the KPIs to see how the stock of interest performs compared to its peers.
        """
    )

if __name__ == "__main__":
    main()