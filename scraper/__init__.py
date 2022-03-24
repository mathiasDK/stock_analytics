from peer_universe import create_peer_df
from information_load import stock_info
import pandas as pd


def create_peer_universe(ticker:str, levels:int=3) -> pd.DataFrame:
    df = create_peer_df(ticker, levels=levels)
    cols = [
        'sector', 'industry', 'currency', 'market_value', 'gross_margin', 
        'ebitda_margin', 'operating_margin', 'enterprise_to_ebitda', 
        'beta', 'forward_pe', 'price_to_book'
    ]
    df[cols] = None
    
    for idx, ticker in enumerate(df.ticker.values):
        print(f'Starting to load information about {ticker}')
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
    return df

if __name__=='__main__':
    df = create_peer_universe('LVMUY')
    print(df)