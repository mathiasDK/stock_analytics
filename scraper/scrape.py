from bs4 import BeautifulSoup 
import pandas as pd
import re
import requests
import urllib.request as ur
import json

def get_linked_tickers(ticker:str, ticker_df_in: pd.DataFrame, peer_group:int) -> pd.DataFrame:
    ticker_df = ticker_df_in.copy()
    print(ticker_df[ticker_df.peer_group==peer_group-1]['ticker'].values)
    for t in ticker_df[ticker_df.peer_group==peer_group-1]['ticker'].values:
        url = f'https://finance.yahoo.com/quote/{t}?p={t}'
        print(url)
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            recommendation_table = soup.find(id='similar-by-symbol') # (id='recommendations-by-symbol')
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
            print(f'It wasn\'t possible to extract data for {t}')
            print(e)

    return ticker_df

def create_peer_df(ticker:str):
    ticker_dict = {
        'ticker': [ticker],
        'sector': [None],
        'industry': [None],
        'market_value': [None],
        'currency': [None],
        'peer_group': [0]
    }

    ticker_dataframe = pd.DataFrame.from_dict(ticker_dict)
    for i in range(1,3):
        ticker_dataframe = get_linked_tickers(ticker, ticker_df_in=ticker_dataframe, peer_group=i)

    return ticker_dataframe.drop_duplicates()

def get_currency(ticker:str):
    try:
        url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com'
        # print(url)
        read_data = ur.urlopen(url).read()
        soup = BeautifulSoup(read_data,'html.parser')
        site_json=json.loads(soup.text)
        currency = site_json['quoteSummary']['result'][0]['earnings']['financialCurrency']
        return currency
    except Exception as e:
        print(e)
        return None

def get_profile(ticker:str):
    try:
        url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com'
        read_data = ur.urlopen(url).read()
        soup = BeautifulSoup(read_data,'html.parser')
        site_json=json.loads(soup.text)

        # Variables:
        sector = site_json['quoteSummary']['result'][0]['summaryProfile']['sector']
        industry = site_json['quoteSummary']['result'][0]['summaryProfile']['industry']
        currency = site_json['quoteSummary']['result'][0]['earnings']['financialCurrency']
        enterpriseValue = site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseValue']['raw']
        return sector, industry, currency, enterpriseValue
    except Exception as e:
        print(e)
        return None, None, None, None

class stock_info:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com'
        self._load_json()
        self.currency_conversion = 1.

    def _load_json(self) -> json:
        read_data = ur.urlopen(self.url).read()
        soup = BeautifulSoup(read_data,'html.parser')
        site_json=json.loads(soup.text)
        self.site_json = site_json
    
    def get_sector(self) -> str:
        """Getting the sector from the summary of the ticker. Returns None if there is an error while loading

        Returns:
            str: The sector
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['summaryProfile']['sector']
        except:
            print(f'It wasn\'t possible to load the sector for {self.ticker}')
            return None

    def get_industry(self) -> str:
        """Getting the industry from the summary of the ticker. Returns None if there is an error while loading

        Returns:
            str: The industry
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['summaryProfile']['industry']
        except:
            print(f'It wasn\'t possible to load the industry for {self.ticker}')
            return None

    def get_currency(self) -> str:
        """Getting the currency from the summary of the ticker. Returns None if there is an error while loading

        Returns:
            str: The industry
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['earnings']['financialCurrency']
        except Exception as e:
            print(f'It wasn\'t possible to load the industry for {self.ticker}', e)
            return None

    def get_market_value(self) -> str:
        """Getting the market_value from the summary of the ticker. Returns None if there is an error while loading
        
        To do:
        - Should be able to handle local currency conversion, so the numbers are comparable

        Returns:
            str: The market value
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseValue']['raw'] * self.currency_conversion
        except:
            print(f'It wasn\'t possible to load the industry for {self.ticker}')
            return None


def test(ticker:str):
    url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com'
    print(url)
    read_data = ur.urlopen(url).read()
    soup = BeautifulSoup(read_data,'html.parser')
    site_json=json.loads(soup.text)
    for k in site_json['quoteSummary']['result'][0]:
        print(k)#['earnings']['financialCurrency']
    print(site_json['quoteSummary']['result'][0]['summaryProfile']['industry'])
    print(site_json['quoteSummary']['result'][0]['summaryProfile']['sector'])
    print(site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseValue']['raw'])

if __name__=='__main__':
    df = create_peer_df('LVMUY')
    for idx, ticker in enumerate(df.ticker.values):
        print(ticker)
        stock_info_ticker = stock_info(ticker)
        # sector, industry, currency, enterpriseValue = get_profile(ticker)
        df.at[idx, 'sector'] = stock_info_ticker.get_sector()
        df.at[idx, 'industry'] = stock_info_ticker.get_industry()
        df.at[idx, 'currency'] = stock_info_ticker.get_currency()
        df.at[idx, 'market_value'] = stock_info_ticker.get_market_value()
        # df.loc[df.ticker==ticker,['sector', 'industry', 'currency']] = get_currency(ticker)
    print(df)
    # get_profile('LVMUY')
    # get_currency('LVMUY')
    # test('LVMUY')