import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
from .styling import PrimaryColors, SecondaryColors, ColorList
import pandas as pd

class Plotter:
    def __init__(self, data:pd.DataFrame, primary_ticker:str, peers:list) -> None:
        """Creating a plotting function primarily to ensure that the coloring is consistent across graphs.

        Args:
            data (pd.DataFrame): A dataframe containing all data that can be plotted.
            primary_ticker (str): The primary ticker used to make sure that this ticker is highlighted
            peers (list): A list of peers.
        """
        self.data = data
        self.primary_ticker = primary_ticker
        self.peers = peers
        self._create_color_dict()

    def _create_color_dict(self) -> None:
        """Creating a dictionary containing each ticker and a corresponding color to ensure that the coloring is consistent across graphs.
        """
        self.color_dict = {
            str(self.primary_ticker): PrimaryColors.ORANGE.value
        }
        color_list = self._get_color_list()
        for peer, color in zip(self.peers, color_list):
            self.color_dict[peer] = color

    def _get_color_list(self) -> list:
        """Creating a list of colors for each peer (not the primary ticker).
        Depending on the number of peers a list will be provided from the styling.py file.
        If there are more than 5 peers then a list of colors are created ranging from the start color to the end color.

        Returns:
            list: The list of colors for each peer.
        """
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

    def _convert_numbers(self, number_list:list)->list:
        """Converting a list of numbers into a list of strings that are ready to be plotted. 
        Converting large numbers to smaller numbers and adding the abbreviation for it.

        Args:
            number_list (list): A list of numbers

        Returns:
            list: A list of strings with rounded numbers in the smallest possible format.
        """
        try:
            max_value = max(number_list)
            if max_value / 1e12 > 1:
                number_list = [str(round(val*1./1e12, 1))+"T" for val in number_list]
            elif max_value / 1e9 > 1:
                number_list = [str(round(val*1./1e9, 1))+"B" for val in number_list]
            elif max_value / 1e6 > 1:
                number_list = [str(round(val*1./1e6, 1))+"M" for val in number_list]
            elif max_value / 1e3 > 1:
                number_list = [str(round(val*1./1e3, 1))+"K" for val in number_list]
            else:
                number_list = [str(round(val*1./1, 1)) for val in number_list]
            return number_list
        except:
            number_list = [str(round(val*1./1, 1)) for val in number_list]
            return number_list

    def bar(self, y_col:str, mask:list, **kwargs):
        """Creating a bar plot using the plotly.express.bar function. 
        The kwargs go into the bar function.

        Args:
            y_col (str): The y column that should be plotted from the dataframe inputted in the object.
            mask (list): Since the full dataframe contains observations for multiple dates, then a boolean list is inputted to filter the dataframe.

        Returns:
            go.Figure: The bar plot.
        """
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
                text = self._convert_numbers(y.tolist()),
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
        """Creating a line plot using the plotly.express.line function. 
        The kwargs go into the line function.

        Args:
            y_col (str): The y column that should be plotted from the dataframe inputted in the object.

        Returns:
            go.Figure: The line plot.
        """
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