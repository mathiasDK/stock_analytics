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

    def _forecast(self, sales_growth_yearly:float=None):
        if isinstance(sales_growth_yearly, None):
            sales_growth_yearly=self.sales_growth_yearly
        self.forecasted_df = pd.DataFrame()
        self.forecasted_df['year'] = range(1, self.forecast_period+1)
        self.forecasted_df['sales'] = [self.current_sales*(1+sales_growth_yearly)**t for t in range(self.forecast_period)]
        self.forecasted_df['ebit_margin'] = np.linspace(start=self.ebit_margin_current, stop=self.ebit_margin_future, num=self.forecast_period)
        self.forecasted_df['pe_ratio'] = np.linspace(start=self.pe_ratio_current, stop=self.pe_ratio_future, num=self.forecast_period)
        self.forecasted_df['ebit'] = self.forecasted_df['sales'] * self.forecasted_df['ebit_margin']
        self.forecasted_df['valuation'] = self.forecasted_df['ebit'] * self.forecasted_df['pe_ratio']

    def get_cagr(self):
        cagr = (self.forecasted_df.iloc[-1]['valuation'] / self.forecasted_df.iloc[0]['valuation'])**(1/self.forecast_period)-1 + self.dividend
        return cagr

    def cagr_sensitivity(self):
        pass

    def get_forecast(self):
        return self.forecasted_df

ve = valuation_engine(
    sales_growth_yearly = 0.08,
    ebit_margin_current = 0.076,
    ebit_margin_future = 0.08,
    pe_ratio_current = 16.4,
    pe_ratio_future = 16.4,
    dividend = 0.035,
    forecast_period = 5,
    current_sales = 1000
)
print(ve.get_cagr())
print(ve.forecasted_df)
