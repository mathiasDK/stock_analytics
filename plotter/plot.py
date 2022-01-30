from turtle import width
import plotly.graph_objects as go



class plot:
    """
    This class will be used to create all necessary plots in a consistent format.
    """

    def __init__(self, fig=None, width=800, height=400, title_size=14, tick_size=8, axis_size=10, font_size=8) -> None:
        if not fig:
            self.fig = go.Figure()
        else:
            self.fig = fig
        self.width = width
        self.height = height
        self.title_size = title_size
        self.tick_size = tick_size
        self.axis_size = axis_size
        self.font_size = font_size
        self.margin = {
            't': 0,
            'b': 0,
            'l': 0,
            'r': 0
        }
        self.font_family = 'Arial'
        self.colorDict = {
                'primary': '#1C4C38', 
                'secondary': '#005288',
                'first_grey': '#C4C4C4', 
                'light_grey': '#f9f9f9'
        }
        self.colorList = [
                '#005288', 
                '#1C4C38',
                '#01B2B3', 
                '#DD663C', 
                '#A899A5', 
                '#492a42', 
                '#d8eded', 
                '#bdd7e5', 
                '#bdd7e5'
            ]

    def _set_layout(self) -> None:
        """A function to format the plot into the chosen layout
        It should be run after each plotting function.
        """

        layout = go.Layout(
            height=self.height,
            width=self.width,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        self.fig.update_layout(layout)
        self.fig.update_xaxes(linewidth = 1, linecolor ='black')
        self.fig.update_yaxes(linewidth = 1, linecolor = 'black')

    def _set_end_label(self, x, y, text, color):
        """This function should be used to create labels at the right side of the graph

        Args:
            x (float): The most right variable on the x axis
            y (float): The height of the label
            text (str): The label text
            color (str): The hex color of the text (same as line)
        """

        # Making room for the labels
        self.margin['r'] = 10
        self.fig.add_annotation(
            x=x,
            y=y,
            xref="x",
            yref="y",
            text=text,
            font=dict(
                family=self.font_family,
                size=self.font_size,
                color=color
                ),
            align="left"
        )

    def bar_grouped(x, y, group, barmode='stack', x_title=None, y_title=None, title=None):
        pass

    def bar(x, y, x_title=None, y_title=None, title=None):
        pass

    def continuous_grouped(x, y, group, markers='line', x_title=None, y_title=None, title=None):
        pass

    def continuous(x, y, markers='line', x_title=None, y_title=None, title=None):
        pass

