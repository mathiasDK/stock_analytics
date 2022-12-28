import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

class plot:
    """
    This class will be used to create all necessary plots in a consistent format.
    """

    def __init__(self, fig=None, width=800, height=400, title_size=14, tick_size=10, axis_size=10, font_size=10, show_fig=False) -> None:
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
            't': 30,
            'b': 10,
            'l': 10,
            'r': 10
        }
        self.font_family = 'Arial'
        self.colorDict = {
                'primary': '#1C4C38', 
                'secondary': '#005288',
                'first_grey': '#C4C4C4', 
                'light_grey': '#f9f9f9',
                'white_background': '#faf8f0'
        }
        self.colorList = [
                '#005288', 
                '#1C4C38',
                '#01B2B3', 
                '#DD663C', 
                '#A899A5', 
                '#492a42', 
                '#d8eded', 
                '#bdd7e5'
            ]
        self.show_legend = True

    def _set_layout(self, x_label=None, y_label=None, title=None, legend_title=None) -> None:
        """
        A function to format the plot into the chosen layout
        It should be run after each plotting function.
        """

        layout = go.Layout(
            height=self.height,
            width=self.width,
            paper_bgcolor=self.colorDict.get('white_background'),
            plot_bgcolor=self.colorDict.get('white_background'),
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
            showlegend=self.show_legend,
            colorway=self.colorList
        )

        self.fig.update_layout(layout)
        self.fig.update_xaxes(linewidth = 1, linecolor ='black', tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size))
        self.fig.update_yaxes(linewidth = 1, linecolor = 'black', tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size))

    def get_layout(self, x_label=None, y_label=None, title=None, legend_title=None) -> None:
        """
        A function to format the plot into the chosen layout
        It should be run after each plotting function.
        """

        layout = go.Layout(
            height=self.height,
            width=self.width,
            paper_bgcolor=self.colorDict.get('white_background'),
            plot_bgcolor=self.colorDict.get('white_background'),
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
            showlegend=self.show_legend,
            colorway=self.colorList
        )

        self.fig.update_layout(layout)
        self.fig.update_xaxes(linewidth = 1, linecolor ='black', tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size), showgrid=False)
        self.fig.update_yaxes(linewidth = 1, linecolor = 'black', tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size), showgrid=False)

        """
        try:
            colormap={}
            for i in range(len(self.fig.data)):
                key=self.fig.data[i]['name']
                colormap[key]=self.colorList[i]
        """

        return self.fig.layout


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
        self.show_legend=False

    def to_and_from_lines_text(
        self, 
        x_start=None, x_end=None, text="",
        x_start_index:float=None, x_end_index:float=None,
        y:float=None, y_start:float=None, y_end:float=None, y_offset:float=0.1,
        **kwargs)->None:
        
        # Setting the variables:
        x_start=self.fig.data['x'].index(x_start) if x_start is not None else x_start_index
        x_end=self.fig.data['x'].index(x_end) if x_end is not None else x_end_index
        y_start_start=y_start if y_start is not None else y*(1-y_offset)
        y_end_start=y_end if y_end is not None else y*(1-y_offset)

        self.fig.add_shape( # First upright line
            type='line',
            x0=x_start, x1=x_start,
            y0=y_start_start, y1=y,
            line=dict(color="#000000",width=1),
            **kwargs
        )
        self.fig.add_shape( # Last upright line
            type='line',
            x0=x_end, x1=x_end,
            y0=y_end_start, y1=y,
            line=dict(color="#000000",width=1),
            **kwargs
        )
        self.fig.add_shape( # Horizontal line
            type='line',
            x0=x_start, x1=x_end,
            y0=y, y1=y,
            line=dict(color="#000000",width=1),
            **kwargs
        ),
        self.fig.add_annotation(
            text=text,
            x=(x_end-x_start)/2.+x_start,
            y=y,
            bgcolor=self.colorDict.get('white_background'),
            showarrow=False,
            borderpad=8,
            font=dict(size=self.font_size+2, color='#000000'),
            **kwargs
        )

import plotly_theme
def main():
    x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'] 
    y = [1,2,3,4,5,6,7,8,9]
    group = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'] 
    

    # fig=go.Figure()
    # # fig.layout=plot(fig).get_layout(title='TEST TITLE', x_label='X axis', y_label='Y axis')
    # # for x_val,y_val,name in zip(x,y,group):
    # #     fig.add_traces(go.Bar(x=[x_val], y=[y_val], name='a', marker_line=dict(width=0.5, color='#222222')))
    # fig.add_trace(go.Bar(x=x, y=y, marker_line=dict(width=5.5, color='#995599')))

    # # fig_obj=plot(fig)
    # # fig_obj.to_and_from_lines_text(x_start_index=1, x_end_index=4, text="TEST", y=5)
    # # fig=fig_obj.fig
    # print(fig.layout.template)
    # fig.show()
    # print(templated_fig.layout.template)
    # template=pio.to_templated(fig.layout)
    # print(template)
    fig=px.bar(x=x, y=y, color=group, template="master")
    # print(fig.layout.template.layout)
    fig.show()
    fig=px.line(x=x, y=y, template="master")
    # print(fig.layout.template.layout)
    fig.show()


if __name__=='__main__':
    main()