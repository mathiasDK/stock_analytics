from bs4 import BeautifulSoup
import urllib.request as ur
import json
import pandas as pd

class YahooExtractor:
    def __init__(self, ticker:str):
        self.ticker = ticker

    def get_stats(self) -> pd.DataFrame:
        """Extracting the stats for the selected ticker from yahoo finance.

        Returns:
            pd.DataFrame: A dataframe containing the stats of the ticker.
        """
        url = f"https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self.ticker}?lang=en-US&region=US&symbol={self.ticker}&padTimeSeries=true&type=quarterlyMarketCap%2CtrailingMarketCap%2CquarterlyEnterpriseValue%2CtrailingEnterpriseValue%2CquarterlyPeRatio%2CtrailingPeRatio%2CquarterlyForwardPeRatio%2CtrailingForwardPeRatio%2CquarterlyPegRatio%2CtrailingPegRatio%2CquarterlyPsRatio%2CtrailingPsRatio%2CquarterlyPbRatio%2CtrailingPbRatio%2CquarterlyEnterprisesValueRevenueRatio%2CtrailingEnterprisesValueRevenueRatio%2CquarterlyEnterprisesValueEBITDARatio%2CtrailingEnterprisesValueEBITDARatio&merge=false&period1=493590046&period2=1690014975&corsDomain=finance.yahoo.com"

        stat_dict = self._get_readable_json(url)

        # Starting to input data into the dataframe.
        df = pd.DataFrame(
            columns=["metric", "date", "value"]
        )

        for i in range(len(stat_dict["timeseries"]["result"])):
            # Looping through each metric and putting it into dataframe if possible.
            stats = stat_dict["timeseries"]["result"][i]

            metric = stats["meta"]["type"][0]

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
                # If it isn't possible to extract the data then continue to the next metric.
                continue

        return df

    def get_potential_metrics(self) -> list:
        """Creating a list of metrics that are included the dataframe.

        Returns:
            list: A list of unique metrics for the given ticker.
        """
        df = self.get_stats()
        return df["metric"].unique().tolist()

    def get_recommended_symbols(self) -> list:
        """Getting a list of symbols that yahoo calls recommended.

        Returns:
            list: The list of recommended tickers.
        """
        url = f"https://query1.finance.yahoo.com/v6/finance/recommendationsbysymbol/{self.ticker}?"

        try:
            symbol_json = self._get_readable_json(url)
            s = symbol_json['finance']['result'][0]['recommendedSymbols']
            symbols = [val["symbol"] for val in s]

            return symbols
        except:
            print("Didn't find any recommended symbols")
            return None

    def _get_readable_json(self, url) -> dict:
        """Converting the url into a more readable format that can then be structured for some valid output.

        Args:
            url (str): The url which should be converted into a more readable format.

        Returns:
            dict: The url in a more readable format.
        """
        read_data = ur.urlopen(url).read() 
        soup_stat = BeautifulSoup(read_data,'lxml')
        output_string = str(soup_stat.find_all('p')[0])[3:-4] # Trimming the html string to a json convertible string
        output_json = json.loads(output_string)

        return output_json

if __name__=="__main__":
    orsted = YahooExtractor("ORSTED.CO")
    print(orsted.get_stats())
    print(orsted.get_potential_metrics())
    # print(orsted.get_recommended_symbols())
    # print(get_statistics('ORSTED.CO'))