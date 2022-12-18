import numpy as np

np.random.seed(123)

class forecast_financials:
    # Source of inspiration: https://www.linkedin.com/pulse/how-assess-value-company-combining-discounted-cash-anthony/
    
    def __init__(self, n_periods, n_shares, wacc:float, perpetual_rate:float, n_samples:int) -> None:
        self.n_periods=n_periods
        self.n_shares=n_shares
        self.wacc=wacc
        self.perpetual_rate=perpetual_rate
        self.tax_rate=0.2
        self.n_samples=n_samples

        self.arr_periods=np.ones((self.n_samples, self.n_periods))*np.linspace(1, self.n_periods, self.n_periods)

    def set_revenue(self, current_revenue:float, estimated_future_revenue:float, uncertainty_pct:float=0.1) -> None:
        """Setting some key revenue metrics which can be used for further calculations. Note that it must be a value in a fiscal year.

        Args:
            current_revenue (float): What is the current revenue in the latest fiscal year
            estimated_future_revenue (float): What is the estimated revenue n_periods into the future
            uncertainty_pct (float, optional): 
                How much do you estimate the revenue can deviate in the future, this is translated into a standard deviation, 
                thus 10% means a standard deviation of 10 % of the revenue forecast. Defaults to 0.1.
        """
        self.current_revenue=current_revenue
        self.estimated_future_revenue=estimated_future_revenue
        self.estimated_future_revenue_uncertainty=estimated_future_revenue*uncertainty_pct

    def set_gross_margin(self, current_gross_margin:float, estimated_gross_margin:float, uncertainty_pct:float=0.2) -> None:
        """Setting key metrics for gross profit margin n periods into the future.
        If it is a growth company then it can be useful to find inspiration in mature companies gross profit margins.

        Args:
            current_gross_margin (float): What is the gross profit margin for the current FY.
            estimated_gross_margin (float): What is the gross profit margin n periods into the future.
            uncertainty_pct (float, optional): This is used to calculate a standard deviation of the gross profit. Defaults to 0.2.
        """
        self.current_gross_margin=current_gross_margin
        self.estimated_gross_margin=estimated_gross_margin
        self.estimated_gross_margin_uncertainty=estimated_gross_margin*uncertainty_pct

    def set_sga_cost(self, current_pct_of_sales:float, estimated_future_pct_of_sales:float, uncertainty:float=0.1)->None:
        if hasattr(self, 'estimated_future_revenue'):
            self.current_sga_cost=self.current_revenue*current_pct_of_sales
            self.estimated_future_sga_cost=self.estimated_future_revenue*estimated_future_pct_of_sales
            self.estimated_future_sga_cost_uncertainty=self.estimated_future_sga_cost*uncertainty
        else:
            raise Exception('Please set revenue targets first using the set_revenue() function.')

    def set_deprication_amortization(self, pct_of_sales:float, uncertainty:float=0.1)->None:
        if hasattr(self, 'estimated_future_revenue'):
            self.current_dep_amort=self.current_revenue*pct_of_sales
            self.estimated_future_dep_amort=self.estimated_future_revenue*pct_of_sales
            self.estimated_future_dep_amort_uncertainty=self.estimated_future_dep_amort*uncertainty
        else:
            raise Exception('Please set revenue targets first using the set_revenue() function.')

    def set_interest_expenses(self, pct_of_sales:float, yearly_growth_rate:float=0.02, uncertainty:float=0.005)->None:
        if hasattr(self, 'estimated_future_revenue'):
            self.current_interest_expense=self.current_revenue*pct_of_sales
            self.estimated_future_interest_expense=self.estimated_future_revenue*pct_of_sales*(1+yearly_growth_rate)**self.n_periods
            self.estimated_future_interest_expense_uncertainty=self.estimated_future_interest_expense*uncertainty
        else:
            raise Exception('Please set revenue targets first using the set_revenue() function.')

    def set_net_working_capital(self, current_assets:float, current_liabilities:float, estimated_future_assets:float, estimated_future_liabilities:float, uncertainty:float=0.1)->None:
        self.current_nwc=current_assets-current_liabilities
        self.estimated_future_nwc=estimated_future_assets-estimated_future_liabilities
        self.estimated_future_nwc_uncertainty=self.estimated_future_nwc*uncertainty

    def get_revenue(self)->np.ndarray:
        """Create a matrix with a shape of n_samples*n_periods with the estimated revenue in each period for each simulation.
        Each simulation has a CAGR and that CAGR is used for the growth rate of revenue.

        Raises:
            Exception: If the estimated_future_revenue haven't been set through the set_revenue() function, then it will raise an error.

        Returns:
            np.ndarray: An array with shape n_samples*n_periods with the estimated revenue in each period for each simulation.
        """
        if hasattr(self, 'estimated_future_revenue'):
            estimated_revenue_matrix=self._estimated_matrix(self.estimated_future_revenue, self.estimated_future_revenue_uncertainty, self.current_revenue)
            return estimated_revenue_matrix
        else:
            raise Exception('Please set revenue targets first using the set_revenue() function.')

    def get_gross_margin(self)->np.ndarray:
        if hasattr(self, 'estimated_gross_margin'):
            estimated_gross_margin_matrix=self._estimated_matrix(self.estimated_gross_margin, self.estimated_gross_margin_uncertainty, self.current_gross_margin)
            return estimated_gross_margin_matrix
        else:
            raise Exception('Please set gross margin targets first using the set_gross_margin() function.')

    def get_gross_profit(self)->np.ndarray:
        revenue=self.get_revenue()
        gross_margin=self.get_gross_margin()
        gross_profit=revenue*gross_margin
        return gross_profit

    def get_sga(self)->np.ndarray:
        if hasattr(self, 'estimated_future_sga_cost'):
            estimated_sga_matrix=self._estimated_matrix(self.estimated_future_sga_cost, self.estimated_future_sga_cost_uncertainty, self.current_sga_cost)
            return estimated_sga_matrix
        else:
            raise Exception('Please set sga cost targets first using the set_sga_cost() function.')

    def get_dep_amort(self)->np.ndarray:
        if hasattr(self, 'estimated_future_dep_amort'):
            estimated_dep_amort_matrix=self._estimated_matrix(self.estimated_future_dep_amort, self.estimated_future_dep_amort_uncertainty, self.current_dep_amort)
            return estimated_dep_amort_matrix
        else:
            raise Exception('Please set depreciation and amortization targets first using the set_dep_amort() function.')

    def get_interest_expense(self)->np.ndarray:
        if hasattr(self, 'estimated_future_interest_expense'):
            estimated_int_exp_matrix=self._estimated_matrix(self.estimated_future_interest_expense, self.estimated_future_interest_expense_uncertainty, self.current_interest_expense)
            return estimated_int_exp_matrix
        else:
            raise Exception('Please set interest expense targets first using the set_int_exp() function.')

    def get_nwc(self)->np.ndarray:
        if hasattr(self, 'estimated_future_nwc'):
            estimated_nwc_matrix=self._estimated_matrix(self.estimated_future_nwc, self.estimated_future_nwc_uncertainty, self.current_nwc)
            return estimated_nwc_matrix
        else:
            raise Exception('Please set nwc targets first using the set_nwc() function.')

    def get_net_income(self)->np.ndarray:
        gross_profit=self.get_gross_profit()
        sga=-1*self.get_sga()
        dep_amort=self.get_dep_amort()
        int_exp=self.get_interest_expense()
        profit_before_tax=gross_profit+sga+dep_amort+int_exp
        tax=profit_before_tax*self.tax_rate*-1.
        net_income=profit_before_tax+tax
        return net_income

    def get_fcf(self)->np.ndarray:
        gross_profit=self.get_gross_profit()
        sga=-1*self.get_sga()
        dep_amort=self.get_dep_amort()
        capex=dep_amort
        int_exp=self.get_interest_expense()
        profit_before_tax=gross_profit+sga+dep_amort+int_exp
        tax=profit_before_tax*self.tax_rate*-1.
        net_income=profit_before_tax+tax
        nwc=self.get_nwc()
        fcf=net_income-int_exp-dep_amort+nwc+capex
        return fcf

    def get_discount_factor(self)->np.ndarray:
        discount_factor=np.power(1+self.wacc, self.arr_periods)
        return discount_factor

    def get_company_value(self)->np.ndarray:
        fcf=self.get_fcf()
        discount_factor=self.get_discount_factor()
        npv=fcf/discount_factor

        terminal_value=fcf[:,-1]*(1+self.perpetual_rate)/(self.wacc-self.perpetual_rate)/discount_factor[:,-1]
        # print('terminal value:',np.mean(terminal_value))
        # print('npv:',np.mean(np.sum(npv, axis=1)))

        company_value=np.sum(npv, axis=1)+terminal_value
        self.company_value=company_value
        return company_value

    def get_fair_value_per_share(self)->np.array:
        if not hasattr(self, 'company_value'):
            self.get_company_value()
        
        return self.company_value/self.n_shares


    def _estimated_matrix(self, estimate, uncertainty, current):
        arr_estimate=np.random.normal(estimate, uncertainty, self.n_samples)
        arr_cagr=cagr(current, arr_estimate, self.n_periods)
        arr_cagr_multiplier=np.power(1+arr_cagr.reshape(self.n_samples, 1), self.arr_periods)
        estimated_matrix=current*arr_cagr_multiplier
        return estimated_matrix
        

def cagr(start_value, end_value, periods)->float:
    # Make sure that it can handle negative start of end values.
    cagr=(end_value*1./start_value)**(1./periods)-1
    return cagr