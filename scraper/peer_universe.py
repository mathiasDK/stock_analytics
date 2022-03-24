from bs4 import BeautifulSoup 
import pandas as pd
import re
import requests

def get_linked_tickers(ticker_df_in: pd.DataFrame, peer_group:int) -> pd.DataFrame:
    """This method will look into yahoo finance to extract information about other stocks similar to the main stock (ticker)

    Args:
        ticker_df_in (pd.DataFrame): The dataframe containing tickers which will be used to look up peers
        peer_group (int): Iteration of peers - the 'wave' number

    Returns:
        pd.DataFrame: _description_
    """
    ticker_df = ticker_df_in.copy()
    # print(ticker_df[ticker_df.peer_group==peer_group-1]['ticker'].values)
    for t in ticker_df[ticker_df.peer_group==peer_group-1]['ticker'].values:
        url = f'https://finance.yahoo.com/quote/{t}?p={t}'
        # print(url)
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            try:
                # Trying to find symbols that are like the one the code looks at
                recommendation_table = soup.find(id='recommendations-by-symbol') # (id='similar-by-symbol')
            except:
                # If the above fails, then it will look at symbols that other people look at
                recommendation_table = soup.find(id='similar-by-symbol') # (id='similar-by-symbol')

            for c in recommendation_table.find_all(href=True):
                quote_link = c['href']
                x = re.findall('^\/quote\/\w{2,6}', quote_link)
                linked_symbol = x[0][7:]
                linked_symbol_dict = {
                    'ticker': [linked_symbol],
                    'peer_group': [peer_group]
                }
                linked_symbol_df = pd.DataFrame(data=linked_symbol_dict)
                ticker_df = pd.concat([ticker_df, linked_symbol_df], ignore_index=True)
            
        except Exception as e:
            print(f'It wasn\'t possible to find peers to {t}')
            # print(e)

    return ticker_df

def create_peer_df(ticker:str, levels:int=3) -> pd.DataFrame:
    """Creating a single column dataframe containing peers to the ticker.

    Args:
        ticker (str): The main ticker to look for peers to
        levels (int, optional): How many iterations of peers it should loop through. Defaults to 3.

    Returns:
        pd.DataFrame: A single columned dataframe containing unique yahoo finance ticker symbols for peers to the main ticker.
    """
    ticker_dict = {
        'ticker': [ticker],
        'peer_group': [0]
    }

    ticker_dataframe = pd.DataFrame.from_dict(ticker_dict)
    for i in range(1,levels):
        ticker_dataframe = get_linked_tickers(ticker_df_in=ticker_dataframe, peer_group=i)
        ticker_dataframe = ticker_dataframe.groupby('ticker')['peer_group'].min().reset_index()

    ticker_dataframe = ticker_dataframe.drop(columns=['peer_group']).drop_duplicates().reset_index(drop=True)

    return ticker_dataframe

if __name__=='__main__':
    df = create_peer_df('LVMUY')
    print(df)
