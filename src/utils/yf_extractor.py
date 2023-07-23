from bs4 import BeautifulSoup
import urllib.request as ur
import json
# import numpy as np
import pandas as pd

class YahooExtractor:
    def __init__(self, ticker:str):
        self.ticker = ticker

    def get_stats(self) -> pd.DataFrame:
        url = f"https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self.ticker}?lang=en-US&region=US&symbol={self.ticker}&padTimeSeries=true&type=quarterlyMarketCap%2CtrailingMarketCap%2CquarterlyEnterpriseValue%2CtrailingEnterpriseValue%2CquarterlyPeRatio%2CtrailingPeRatio%2CquarterlyForwardPeRatio%2CtrailingForwardPeRatio%2CquarterlyPegRatio%2CtrailingPegRatio%2CquarterlyPsRatio%2CtrailingPsRatio%2CquarterlyPbRatio%2CtrailingPbRatio%2CquarterlyEnterprisesValueRevenueRatio%2CtrailingEnterprisesValueRevenueRatio%2CquarterlyEnterprisesValueEBITDARatio%2CtrailingEnterprisesValueEBITDARatio&merge=false&period1=493590046&period2=1690014975&corsDomain=finance.yahoo.com"

        stat_dict = self._get_readable_json(url)
        df = pd.DataFrame(
            columns=["metric", "date", "value"]
        )

        for i in range(len(stat_dict["timeseries"]["result"])):
            stats = stat_dict["timeseries"]["result"][i]

            metric = stats["meta"]["type"][0]

            # if metric in ["trailingMarketCap", "quarterlyEnterpriseValue", "trailingEnterpriseValue"]:
            #     continue
            try:
                stat_vals = stats[metric]

                stat_dates = []
                stat_values = []
                for stat_val in stat_vals:
                    stat_date = stat_val["asOfDate"]
                    stat_value = stat_val["reportedValue"]["raw"]

                    stat_dates.append(stat_date)
                    stat_values.append(stat_value)

                stat_metrics = [metric]*len(stat_values)
                sub_df = pd.DataFrame(
                    data={
                        "metric": stat_metrics,
                        "date": stat_dates,
                        "value": stat_values
                    }
                )

                df = pd.concat([df, sub_df], ignore_index=True)
            except:
                continue

        return df

    def get_potential_metrics(self):
        df = self.get_stats()
        return df["metric"].unique()

    def get_recommended_symbols(self):
        url = f"https://query1.finance.yahoo.com/v6/finance/recommendationsbysymbol/{self.ticker}?"

        try:
            symbol_json = self._get_readable_json(url)
            s = symbol_json['finance']['result'][0]['recommendedSymbols']
            symbols = [val["symbol"] for val in s]

            return symbols
        except:
            print("Didn't find any recommended symbols")
            return None

    def _get_readable_json(self, url):
        read_data = ur.urlopen(url).read() 
        soup_stat = BeautifulSoup(read_data,'lxml')
        output_string = str(soup_stat.find_all('p')[0])[3:-4] # Trimming the html string to a json convertible string
        output_json = json.loads(output_string)

        return output_json

def get_statistics(ticker):
    """
    Loading key statistics per ticker
    
    """
    url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/" + ticker + "?modules=defaultKeyStatistics"
    print(url)
    read_data = ur.urlopen(url).read() 
    soup_stat = BeautifulSoup(read_data,'lxml')
    output_string = str(soup_stat.find_all('p')[0])[3:-4] # Trimming the html string to a json convertible string
    stat_dict = json.loads(output_string)

    return stat_dict

if __name__=="__main__":
    orsted = YahooExtractor("ORSTED.CO")
    print(orsted.get_stats())
    print(orsted.get_potential_metrics())
    # print(orsted.get_recommended_symbols())
    # print(get_statistics('ORSTED.CO'))