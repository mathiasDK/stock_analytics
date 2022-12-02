import urllib.request as ur
import json
from xml.dom.minidom import Attr
from bs4 import BeautifulSoup 


class stock_info:
    """A class which is used to extract information from Yahoo Finance on a ticker level. The ticker is the primary input of the class.
    The template for the data is: 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com'
    """
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker.upper()
        try:
            self.url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com'
            self._load_json()
        except:
            self.site_json = {}
        self.currency_conversion = 1.
        self.denominator = 1e9

    def _load_json(self) -> json:
        """Opening and parsing the url to make it ready for extracting information
        Returns:
            json: The json which contains data about the ticker
        """
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
            str: The currency
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['earnings']['financialCurrency']
        except:
            try: 
                return self.site_json['quoteSummary']['result'][0]['financialData']['financialCurrency']
            except Exception as e:
                print(f'It wasn\'t possible to load the currency for {self.ticker}', e)
                return None

    def get_market_value(self) -> float:
        """Getting the market_value from the summary of the ticker. Returns None if there is an error while loading
        
        To do:
        - Should be able to handle local currency conversion, so the numbers are comparable
        Returns:
            str: The market value
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseValue']['raw'] * self.currency_conversion / self.denominator
        except:
            print(f'It wasn\'t possible to load the market value for {self.ticker}')
            return None

    def get_gross_margin(self) -> float:
        """Getting the gross margin from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The gross margin
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['financialData']['grossMargins']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the gross margin for {self.ticker}', e)
            return None    

    def get_ebitda_margin(self) -> float:
        """Getting the ebitda margin from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The ebitda margin
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['financialData']['ebitdaMargins']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the ebitda margin for {self.ticker}', e)
            return None
    
    def get_operating_margin(self) -> float:
        """Getting the ebitda margin from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The opearting margin
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['financialData']['operatingMargins']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the operating margin for {self.ticker}', e)
            return None

    def get_enterprise_to_ebitda(self) -> float:
        """Getting the enterprise value to ebitda ratio from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The market cap to ebitda
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseToEbitda']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the enterprise value to ebitda ratio for {self.ticker}', e)
            return None

    def get_beta(self) -> float:
        """Getting the beta from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The beta
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['beta']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the beta for {self.ticker}', e)
            return None

    def get_forward_pe(self) -> float:
        """Getting the forward PE ratio from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The forward PE ratio
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['forwardPE']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the forward PE ratio for {self.ticker}', e)
            return None

    def get_price_to_book(self) -> float:
        """Getting the price to book ratio from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The PB ratio
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['priceToBook']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the PB ratio for {self.ticker}', e)
            return None

    def get_current_ratio(self) -> float:
        """Getting the current ratio from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The current ratio
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['financialData']['currentRatio']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the current ratio for {self.ticker}', e)
            return None

    def get_trailing_earnings_per_share(self) -> float:
        """Getting the trailing earning per share from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The trailing earning per share
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['defaultKeyStatistics']['trailingEps']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the trailingEps ratio for {self.ticker}', e)
            return None

    def get_debt_to_equity_ratio(self) -> float:
        """Getting the debt to equity ratio from the summary of the ticker. Returns None if there is an error while loading
        Returns:
            float: The debtToEquity ratio
        """
        try:
            return self.site_json['quoteSummary']['result'][0]['financialData']['debtToEquity']['raw']
        except Exception as e:
            print(f'It wasn\'t possible to load the debtToEquity ratio for {self.ticker}', e)
            return None


if __name__=='__main__':
    orsted = stock_info('orsted.co')
    print(dir(orsted))
    print(orsted.get_beta())
    print(orsted.get_enterprise_to_ebitda())
    print(orsted.get_debt_to_equity_ratio())

