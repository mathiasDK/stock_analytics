import plotly.graph_objects as go



class plot:
    """
    This class will be used to create all necessary plots in a consistent format.
    """

    def __init__(self, fig=None, width=800, height=400, title_size=14, tick_size=8, axis_size=10, font_size=8, show_fig=False) -> None:
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
        self.show_fig = show_fig
        self.margin = {
            't': 100,
            'b': 100,
            'l': 100,
            'r': 100
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

    def _set_layout(self, x_label=None, y_label=None, title=None, legend_title=None) -> None:
        """
        A function to format the plot into the chosen layout
        It should be run after each plotting function.
        """

        layout = go.Layout(
            height=self.height,
            width=self.width,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(
                font=dict(
                    color='#000000',
                    size=self.title_size
                ),
                text=title
            ),
            margin=self.margin,
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend_title=legend_title,
        )

        self.fig.update_layout(layout)
        self.fig.update_xaxes(linewidth = 1, linecolor ='black', tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size))
        self.fig.update_yaxes(linewidth = 1, linecolor = 'black', tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size))

    def _set_end_label(self, x, y, text, color):
        """
        This function should be used to create labels at the right side of the graph

        Args:
            x (float): The most right variable on the x axis
            y (float): The height of the label
            text (str): The label text
            color (str): The hex color of the text (same as line)
        """

        # Making room for the labels
        self.margin['r'] *= 1.15
        self.fig.add_annotation(
            x=1.05,
            y=y,
            xref="paper",
            yref="y",
            text=text,
            font=dict(
                family=self.font_family,
                size=self.font_size,
                color=color
                ),
            align="left",
            ax=0,ay=0
        )

    def bar_grouped(self,x, y, group, barmode='stack', x_title=None, y_title=None, title=None):
        pass

    def bar(self, x, y, x_title=None, y_title=None, title=None):
        pass

    def continuous_grouped(self, x, y, group, mode='line', x_title=None, y_title=None, title=None):
        pass

    def continuous(self, x, y, name=None, mode='lines', x_title=None, y_title=None, title=None, end_annotation=False):
        self.fig.add_trace(
            go.Scatter(
                x=x, y=y,
                mode=mode,
                name=name,
                marker=dict(color=self.colorDict.get('primary'))
            )
        )
        self._set_layout(x_label=x_title, y_label=y_title, title=title)
        
        if end_annotation:
            self._set_end_label(x=x[-1], y=y[-1], text=name, color=self.colorDict.get('primary'))

        self._set_layout(x_label='X axis', y_label='Y axis', title='Title')
        if self.show_fig:
            self.fig.show()

        return self.fig
        

def main():
    x = [1,2,3,4]
    y = [1,2,3,4]
    plot(show_fig=True).continuous(x, y, 'A', end_annotation=True)

if __name__=='__main__':
    main()