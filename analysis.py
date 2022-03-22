from plotter.plot import plot
from scraper.scrape import create_peer_universe
import plotly.graph_objects as go
import pandas as pd


def create_fig(data:pd.DataFrame, main_ticker:str, metrics:list, title:str=None, normalize:bool=False):
    df = data.copy()
    if normalize:
        for metric in metrics:
            max_value = df[metric].max()
            min_value = df[metric].min()
            df[metric] = (df[metric] - min_value) / (max_value - min_value)
    new_data = df.melt(id_vars=['ticker'], value_vars=metrics).rename(columns={'variable': 'metric', 'value': 'metric_value'})
    new_data['color'] = ['#e03210' if t==main_ticker else '#d7d7d2' for t in new_data.ticker]
    
    df1 = new_data[new_data.ticker!=main_ticker].reset_index(drop=True)
    df2 = new_data[new_data.ticker==main_ticker].reset_index(drop=True)
    new_data = pd.concat([df1, df2], ignore_index=True)

    new_data["metric"].replace(
        {
            'gross_margin': 'Gross Margin', 
            'ebitda_margin': 'Ebitda Margin',
            'operating_margin': 'Operating Margin',
            'enterprise_to_ebitda': 'Enterprise Value to Ebitda', 
            'beta': 'Beta', 
            'forward_pe': 'Forward PE', 
            'price_to_book': 'Price to Book'
        }, 
        inplace=True
    )

    if normalize:
        tickformat='.0'
        hover_template="<b>%{text}</b><br>Normalized %{y}: %{x:,.2f}<br><extra></extra>"
    else:
        tickformat='0%'
        hover_template="<b>%{text}</b><br>%{y}: %{x:,.1%}<br><extra></extra>"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=new_data.metric_value,
            y=new_data.metric,
            mode='markers',
            marker=dict(color=new_data.color, size=10),
            text=new_data.ticker,
            hovertemplate=hover_template
        )
    )
    if normalize:
        tickformat='.0'
    else:
        tickformat='0%'
    fig.update_layout(
        paper_bgcolor='#f9f5ec',
        plot_bgcolor='#f9f5ec',
        height=len(metrics)*70,
        width=600,
        xaxis=dict(
            tickformat=tickformat,
            ticks="outside", 
            tickwidth=1, 
            tickcolor='black', 
            ticklen=5,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#bdada5',
            tickcolor='rgba(0,0,0,0)',
            ticklen=5
        ),
        title=title,
        margin = {
            't': 60,
            'b': 20,
            'l': 20,
            'r': 20
        }
    )
    fig.show()

if __name__=='__main__':
    data = create_peer_universe('LVMUY', 5)
    print(data)
    create_fig(data, 'LVMUY', ['gross_margin', 'ebitda_margin', 'operating_margin'], title='Margins by company')
    create_fig(data, 'LVMUY', ['enterprise_to_ebitda', 'beta', 'forward_pe', 'price_to_book'], title='Normalized ratios by company', normalize=True)
