from tracemalloc import stop
import pandas as pd
import numpy as np

class valuation_engine:
    def __init__(
        self,
        sales_growth_yearly:float,
        ebit_margin_current:float, 
        ebit_margin_future:float, 
        pe_ratio_current:float, 
        pe_ratio_future:float, 
        dividend:float, 
        forecast_period:float, 
        current_sales:float
        ) -> None:
        self.sales_growth_yearly=sales_growth_yearly
        self.ebit_margin_current=ebit_margin_current
        self.ebit_margin_future=ebit_margin_future
        self.pe_ratio_current=pe_ratio_current
        self.pe_ratio_future=pe_ratio_future
        self.dividend=dividend
        self.forecast_period=forecast_period
        self.current_sales=current_sales
        self._forecast()

    def _forecast(self):
        self.forecasted_df = pd.DataFrame()
        self.forecasted_df['year'] = range(1, self.forecast_period+1)
        self.forecasted_df['sales'] = [self.current_sales*(1+self.sales_growth_yearly)**t for t in range(self.forecast_period)]
        self.forecasted_df['ebit_margin'] = np.linspace(start=self.ebit_margin_current, stop=self.ebit_margin_future, num=self.forecast_period)
        self.forecasted_df['pe_ratio'] = np.linspace(start=self.pe_ratio_current, stop=self.pe_ratio_future, num=self.forecast_period)
        self.forecasted_df['ebit'] = self.forecasted_df['sales'] * self.forecasted_df['ebit_margin']
        self.forecasted_df['valuation'] = self.forecasted_df['ebit'] * self.forecasted_df['pe_ratio']

    def get_cagr(self):
        cagr = (self.forecasted_df.iloc[-1]['valuation'] / self.forecasted_df.iloc[0]['valuation'])**(1/self.forecast_period)-1 + self.dividend
        return cagr

    def _calc_cagr(self, sales_growth_yearly:float=None, ebit_margin_future:float=None, pe_ratio_future:float=None):
        if sales_growth_yearly is None:
            sales_growth_yearly = self.sales_growth_yearly
        if ebit_margin_future is None:
            ebit_margin_future = self.ebit_margin_future
        if pe_ratio_future is None:
            pe_ratio_future = self.pe_ratio_future
        sales = [self.current_sales*(1+sales_growth_yearly)**t for t in range(self.forecast_period)]
        ebit_margin = np.linspace(start=self.ebit_margin_current, stop=ebit_margin_future, num=self.forecast_period)
        pe_ratio = np.linspace(start=self.pe_ratio_current, stop=pe_ratio_future, num=self.forecast_period)
        ebit = sales * ebit_margin
        valuation = ebit * pe_ratio
        cagr = (valuation[-1] / valuation[0])**(1/self.forecast_period)-1
        return cagr

    def cagr_sensitivity(self, sensitivity_ranges:dict=None, steps:int=31):
        sales_growth_range = 0.02
        ebit_margin_range = 0.0
        pe_ratio_range = 0
        sales_growth = np.column_stack(
            (
                list(np.linspace(start=1+self.sales_growth_yearly - sales_growth_range, stop=1+self.sales_growth_yearly + sales_growth_range, num=steps)),
                list(np.power(np.linspace(start=1+self.sales_growth_yearly - sales_growth_range, stop=1+self.sales_growth_yearly + sales_growth_range, num=steps), self.forecast_period))
            )
        ).transpose()
        ebit_margin = np.column_stack(
            (
                list(np.linspace(start=self.ebit_margin_current - ebit_margin_range, stop=self.ebit_margin_current + ebit_margin_range, num=steps)),
                list(np.linspace(start=self.ebit_margin_future - ebit_margin_range, stop=self.ebit_margin_future + ebit_margin_range, num=steps))
            )
        ).transpose()
        pe_ratio = np.column_stack(
            (
                list(np.linspace(start=self.pe_ratio_current - pe_ratio_range, stop=self.pe_ratio_current + pe_ratio_range, num=steps)),
                list(np.linspace(start=self.pe_ratio_future - pe_ratio_range, stop=self.pe_ratio_future + pe_ratio_range, num=steps))
            )
            
        ).transpose()

        sales = self.current_sales * sales_growth
        ebit = sales * ebit_margin
        valuation = ebit * pe_ratio
        cagrs = (valuation[1] / valuation[0])**(1/self.forecast_period)-1

        df = pd.DataFrame(
            {
                'sales_growth': list(np.linspace(start=self.sales_growth_yearly - sales_growth_range, stop=self.sales_growth_yearly + sales_growth_range, num=steps)),
                'ebit_margin_future': list(np.linspace(start=self.ebit_margin_future - ebit_margin_range, stop=self.ebit_margin_future + ebit_margin_range, num=steps)),
                'pe_ratio_future': list(np.linspace(start=self.pe_ratio_future - pe_ratio_range, stop=self.pe_ratio_future + pe_ratio_range, num=steps)),
                'cagr': cagrs
            }
        )
        return df

    def get_forecast(self):
        return self.forecasted_df

ve = valuation_engine(
    sales_growth_yearly = 0.08,
    ebit_margin_current = 0.08,
    ebit_margin_future = 0.08,
    pe_ratio_current = 16.4,
    pe_ratio_future = 16.4,
    dividend = 0.035,
    forecast_period = 5,
    current_sales = 1000
)
a = ve.cagr_sensitivity(steps=5)
print(a)

def test():
    forecast_values = 31
    sales_growth = np.column_stack(
        (
            list(np.linspace(start=1.06, stop=1.1, num=forecast_values)),
            list(np.power(np.linspace(start=1.06, stop=1.1, num=forecast_values), 5))
        )
    ).transpose()
    ebit_margin = np.tile(np.linspace(start=0.08, stop=0.08, num=forecast_values), (2,1))
    pe_ratio = np.tile(np.linspace(start=16.4, stop=16.4, num=forecast_values), (2,1))
    sales = 1000 * sales_growth
    ebit = sales * ebit_margin
    valuation = ebit * pe_ratio
    valuations = (valuation[1] / valuation[0])**(1/5)-1
    df = pd.DataFrame(
        {
            'sales_growth': list(np.linspace(start=1.06, stop=1.1, num=forecast_values)),
            'yield': valuations
        }
    )
    print(df)
