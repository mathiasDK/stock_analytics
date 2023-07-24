import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
from styling import PrimaryColors, SecondaryColors, ColorList
import pandas as pd

class Plotter:
    def __init__(self, data:pd.DataFrame, primary_ticker:str, peers:list) -> None:
        self.data = data
        self.primary_ticker = primary_ticker
        self.peers = peers
        self._create_color_dict()

    def _create_color_dict(self) -> None:
        self.color_dict = {
            str(self.primary_ticker): PrimaryColors.ORANGE.value
        }
        color_list = self._get_color_list()
        for peer, color in zip(self.peers, color_list):
            self.color_dict[peer] = color

    def _get_color_list(self) -> list:
        if len(self.peers)==1:
            return ColorList.ONE.value
        elif len(self.peers)==2:
            return ColorList.TWO.value
        elif len(self.peers)==3:
            return ColorList.THREE.value
        elif len(self.peers)==4:
            return ColorList.FOUR.value
        elif len(self.peers)==5:
            return ColorList.FIVE.value
        else:
            start_color = pc.label_rgb(pc.hex_to_rgb(SecondaryColors.PURPLE.value))
            end_color = pc.label_rgb(pc.hex_to_rgb(SecondaryColors.LAVENDER.value))
            color_list = pc.n_colors(start_color, end_color, len(self.peers), colortype="rgb")
            return color_list

    def bar(self, y_col:str, mask:list, **kwargs):
        df = self.data.copy()
        df = df[mask].sort_values(by=[y_col], ascending=[False])

        # Creating the color list
        tickers = df["ticker"].drop_duplicates().tolist()
        colors = [self.color_dict.get(ticker) for ticker in tickers]
        x = df["ticker"]
        y = df[y_col]
        fig = go.Figure(
            data=[go.Bar(
                x = x,
                y = y,
                marker_color = colors,
                text = [f"{str(round(val,1))}" for val in y],
                **kwargs
            )]
        )
        fig.update_layout(
            yaxis=dict(rangemode="tozero", title=None),
            xaxis=dict(title=None),
            title=f"{y_col} by Ticker"
        )
        return fig

    def line(self, y_col:str, **kwargs):
        fig = px.line(
            self.data,
            x = "date",
            y = y_col,
            color = "ticker",
            color_discrete_map = self.color_dict,
            **kwargs
        )
        fig.update_layout(
            yaxis=dict(rangemode="tozero", title=None),
            xaxis=dict(title=None),
            title=f"Development in {y_col} by Ticker"
        )
        return fig

if __name__=="__main__":
    df = pd.DataFrame(
        data={
            "date": [
                1,2,
                1,2,
                1,2,
                1,2,
                1,2,
                1,2,
                1,2,
            ],
            "value": [
                2,0,
                4,2,
                3,5,
                2,5,
                2,3,
                4,5,
                2,1,
            ],
            "ticker": [
                "ORSTED.CO", "ORSTED.CO", 
                "VWS.CO", "VWS.CO", 
                "DANSKE.CO", "DANSKE.CO", 
                "AAPL", "AAPL", 
                "A", "A", 
                "B", "B",
                "C", "C"]
        }
    )
    primary_ticker = "ORSTED.CO"
    peers = ["VWS.CO", "DANSKE.CO", "AAPL", "A","B","C"]

    # Plotter(df.loc[0,2], primary_ticker=primary_ticker, peers=peers).bar()
    p = Plotter(df, primary_ticker=primary_ticker, peers=peers)
    p.line(y_col="value").show()
    p.bar(y_col="value", mask=[True, False, True, False, True, False, True, False]).show()