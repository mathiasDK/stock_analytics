# from plotter.plot import plot
# from scraper.peer_universe import create_peer_universe
# from scraper import stock_info, create_peer_df
from scraper.peer_universe import create_peer_df
from scraper.information_load import stock_info
import plotly.graph_objects as go
import pandas as pd

def create_peer_universe(ticker:str, levels:int=3) -> pd.DataFrame:
    df = create_peer_df(ticker, levels=levels)
    return df

def add_statistics_to_dataframe(df):
    cols = [
        'sector', 'industry', 'currency', 'market_value', 'gross_margin', 
        'ebitda_margin', 'operating_margin', 'enterprise_to_ebitda', 
        'beta', 'forward_pe', 'price_to_book', 'current_ratio', 'trailing_eps',
        'debt_to_equity'
    ]
    df[cols] = None

    for idx, ticker in enumerate(df.ticker.values):
        print(f'# Starting to load information about {ticker}')
        stock_info_ticker = stock_info(ticker)
        df.at[idx, 'sector'] = stock_info_ticker.get_sector()
        df.at[idx, 'industry'] = stock_info_ticker.get_industry()
        df.at[idx, 'currency'] = stock_info_ticker.get_currency()
        df.at[idx, 'market_value'] = stock_info_ticker.get_market_value()
        df.at[idx, 'gross_margin'] = stock_info_ticker.get_gross_margin()
        df.at[idx, 'operating_margin'] = stock_info_ticker.get_operating_margin()
        df.at[idx, 'ebitda_margin'] = stock_info_ticker.get_ebitda_margin()
        df.at[idx, 'enterprise_to_ebitda'] = stock_info_ticker.get_enterprise_to_ebitda()
        df.at[idx, 'beta'] = stock_info_ticker.get_beta()
        df.at[idx, 'forward_pe'] = stock_info_ticker.get_forward_pe()
        df.at[idx, 'price_to_book'] = stock_info_ticker.get_price_to_book()
        df.at[idx, 'current_ratio'] = stock_info_ticker.get_current_ratio()
        df.at[idx, 'trailing_eps'] = stock_info_ticker.get_trailing_earnings_per_share()
        df.at[idx, 'debt_to_equity'] = stock_info_ticker.get_debt_to_equity_ratio()

    return df

def create_fig(data_peers:pd.DataFrame, main_ticker:str, metrics:list, title:str=None, normalize:bool=False):
    df = data_peers.copy()
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
            'price_to_book': 'Price to Book',
            'current_ratio': 'Current Ratio',
            'trailing_eps': 'Trailing Earnings per Share',
            'debt_to_equity': 'Debt to Equity',
        }, 
        inplace=True
    )

    if normalize:
        tickformat='.0'
        hover_template="<b>%{text}</b><br>Normalized %{y}: %{x:,.2f}<br><extra></extra>"
        x_min = 0
        x_max = 1
        x_range=[x_min, x_max]
    else:
        tickformat='0%'
        hover_template="<b>%{text}</b><br>%{y}: %{x:,.1%}<br><extra></extra>"
        x_min = max(new_data.metric_value.min(), -2)
        x_max = new_data.metric_value.max()
        x_range=[x_min, x_max]

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
            zeroline=False,
            range=x_range
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

peer_dict = {
    'automotive': ['VOLCAR-B.ST', 'VOW3.DE', 'PAH3.DE', 'BMW.DE', 'F', 'GM', 'TM', 'HMC', 'PSNY', 'HOG'],
    'electric_automotive': ['PSNY', 'TSLA', 'NIO', 'RIVN', 'LCID'],
    'transportation': ['DSV.CO', 'MAERSK-B.CO','TRMD-A.CO', 'DNORD.CO', 'DFDS.CO', 'NTG.CO', 'FDX'],
    'healthcare': ['NOVO-B.CO', 'BAVA.CO', 'GMAB.CO', 'SNY', 'AZN', 'JNJ', 'PFE', 'MRK', 'LLY'],
    'consumer_defensives': ['WMT', 'PG', 'KO', 'PEP', 'COST', 'UL', 'TGT', 'KHC', 'CL', 'K', 'CARL-B.CO', 'RBREW.CO'],
    'beverages': ['PEP', 'KO', 'CARL-B.CO', 'RBREW.CO', 'SAM']
}

if __name__=='__main__':
    ticker = 'ORSTED.CO'.upper() #'LMVUY'

    #ticker_df=create_peer_df(ticker, levels=3)
    #data = create_peer_universe(ticker, 5)
    data=pd.DataFrame(
        data={
            'ticker': peer_dict.get('electric_automotive') #['VOLCAR-B.ST', 'VOW3.DE', 'PAH3.DE', 'BMW.DE', 'F', 'GM']
        }
    )
    data=add_statistics_to_dataframe(data)
    create_fig(data, 'PSNY', ['gross_margin', 'ebitda_margin', 'operating_margin'], title='Margins by company')
    create_fig(data, 'PSNY', ['enterprise_to_ebitda', 'beta', 'forward_pe', 'price_to_book', 'debt_to_equity', 'trailing_eps', 'current_ratio'], title='Normalized ratios by company', normalize=True)
