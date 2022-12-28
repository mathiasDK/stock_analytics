import numpy as np


class forecast_financials:
    # Source of inspiration: https://www.linkedin.com/pulse/how-assess-value-company-combining-discounted-cash-anthony/

    def __init__(self, **kwargs) -> None:
        """This function will forecast the financials of a company with a given set of input and then do a set of simulations with some different scenarios to get
        the most accurate picture of where a company x periods into the future.

        - Revenue input:
            - current_revenue (float): What is the current revenue in the latest fiscal year
            - estimated_future_revenue (float): What is the estimated revenue n_periods into the future
            - uncertainty_pct (float, optional):
                - How much do you estimate the revenue can deviate in the future, this is translated into a standard deviation,
                  thus 10% means a standard deviation of 10 % of the revenue forecast. Defaults to 0.1.
        - Gross margin input:
          If it is a growth company then it can be useful to find inspiration in mature companies gross profit margins.
            - current_gross_margin (float): What is the gross profit margin for the current FY.
            - estimated_gross_margin (float): What is the gross profit margin n periods into the future.
            - uncertainty_pct (float, optional): This is used to calculate a standard deviation of the gross profit. Defaults to 0.2.
        """

        valid_args = [
            "current_revenue",
            "estimated_future_revenue",
            "estimated_future_revenue_uncertainty",
            "current_gross_margin",
            "estimated_gross_margin",
            "estimated_gross_margin_uncertainty",
            "current_sga_cost",
            "estimated_future_sga_cost",
            "estimated_future_sga_cost_uncertainty",
            "current_dep_amort",
            "estimated_future_dep_amort",
            "estimated_future_dep_amort_uncertainty",
            "current_interest_expense",
            "estimated_future_interest_expense",
            "estimated_future_interest_expense_uncertainty",
            "current_nwc",
            "estimated_future_nwc",
            "estimated_future_nwc_uncertainty",
            "n_periods",
            "n_shares",
            "wacc",
            "perpetual_rate",
            "n_samples",
            "tax_rate",
        ]
        for arg in valid_args:
            setattr(self, arg, kwargs.get(arg))

        self.arr_periods = np.ones((self.n_samples, self.n_periods)) * np.linspace(
            1, self.n_periods, self.n_periods
        )

    def get_revenue(self) -> np.ndarray:
        """Create a matrix with a shape of n_samples*n_periods with the estimated revenue in each period for each simulation.
        Each simulation has a CAGR and that CAGR is used for the growth rate of revenue.

        Raises:
            Exception: If the estimated_future_revenue haven't been set through the set_revenue() function, then it will raise an error.

        Returns:
            np.ndarray: An array with shape n_samples*n_periods with the estimated revenue in each period for each simulation.
        """
        if hasattr(self, "estimated_future_revenue"):
            estimated_revenue_matrix = self._estimated_matrix(
                self.estimated_future_revenue,
                self.estimated_future_revenue_uncertainty,
                self.current_revenue,
            )
            return estimated_revenue_matrix
        else:
            raise Exception(
                "Please set revenue targets first using the set_revenue() function."
            )

    def get_gross_margin(self) -> np.ndarray:
        if hasattr(self, "estimated_gross_margin"):
            estimated_gross_margin_matrix = self._estimated_matrix(
                self.estimated_gross_margin,
                self.estimated_gross_margin_uncertainty,
                self.current_gross_margin,
            )
            return estimated_gross_margin_matrix
        else:
            raise Exception(
                "Please set gross margin targets first using the set_gross_margin() function."
            )

    def get_gross_profit(self) -> np.ndarray:
        revenue = self.get_revenue()
        gross_margin = self.get_gross_margin()
        gross_profit = revenue * gross_margin
        return gross_profit

    def get_sga(self) -> np.ndarray:
        if hasattr(self, "estimated_future_sga_cost"):
            estimated_sga_matrix = self._estimated_matrix(
                self.estimated_future_sga_cost,
                self.estimated_future_sga_cost_uncertainty,
                self.current_sga_cost,
            )
            return estimated_sga_matrix
        else:
            raise Exception(
                "Please set sga cost targets first using the set_sga_cost() function."
            )

    def get_dep_amort(self) -> np.ndarray:
        if hasattr(self, "estimated_future_dep_amort"):
            estimated_dep_amort_matrix = self._estimated_matrix(
                self.estimated_future_dep_amort,
                self.estimated_future_dep_amort_uncertainty,
                self.current_dep_amort,
            )
            return estimated_dep_amort_matrix
        else:
            raise Exception(
                "Please set depreciation and amortization targets first using the set_dep_amort() function."
            )

    def get_interest_expense(self) -> np.ndarray:
        if hasattr(self, "estimated_future_interest_expense"):
            estimated_int_exp_matrix = self._estimated_matrix(
                self.estimated_future_interest_expense,
                self.estimated_future_interest_expense_uncertainty,
                self.current_interest_expense,
            )
            return estimated_int_exp_matrix
        else:
            raise Exception(
                "Please set interest expense targets first using the set_int_exp() function."
            )

    def get_nwc(self) -> np.ndarray:
        if hasattr(self, "estimated_future_nwc"):
            estimated_nwc_matrix = self._estimated_matrix(
                self.estimated_future_nwc,
                self.estimated_future_nwc_uncertainty,
                self.current_nwc,
            )
            return estimated_nwc_matrix
        else:
            raise Exception(
                "Please set nwc targets first using the set_nwc() function."
            )

    def get_net_income(self) -> np.ndarray:
        gross_profit = self.get_gross_profit()
        sga = -1 * self.get_sga()
        dep_amort = self.get_dep_amort()
        int_exp = self.get_interest_expense()
        profit_before_tax = gross_profit + sga + dep_amort + int_exp
        tax = profit_before_tax * self.tax_rate * -1.0
        net_income = profit_before_tax + tax
        return net_income

    def get_fcf(self) -> np.ndarray:
        gross_profit = self.get_gross_profit()
        sga = -1 * self.get_sga()
        dep_amort = self.get_dep_amort()
        capex = dep_amort
        int_exp = self.get_interest_expense()
        profit_before_tax = gross_profit + sga + dep_amort + int_exp
        tax = profit_before_tax * self.tax_rate * -1.0
        net_income = profit_before_tax + tax
        nwc = self.get_nwc()
        fcf = net_income - int_exp - dep_amort + nwc + capex
        return fcf

    def get_discount_factor(self) -> np.ndarray:
        discount_factor = np.power(1 + self.wacc, self.arr_periods)
        return discount_factor

    def get_company_value(self) -> np.ndarray:
        fcf = self.get_fcf()
        discount_factor = self.get_discount_factor()
        npv = fcf / discount_factor

        terminal_value = (
            fcf[:, -1]
            * (1 + self.perpetual_rate)
            / (self.wacc - self.perpetual_rate)
            / discount_factor[:, -1]
        )

        company_value = np.sum(npv, axis=1) + terminal_value
        self.company_value = company_value
        return company_value

    def get_fair_value_per_share(self) -> np.array:
        if not hasattr(self, "company_value"):
            self.get_company_value()

        return self.company_value / self.n_shares

    def _estimated_matrix(self, estimate, uncertainty, current):
        arr_estimate = np.random.normal(estimate, uncertainty, self.n_samples)
        arr_cagr = cagr(current, arr_estimate, self.n_periods)
        arr_cagr_multiplier = np.power(
            1 + arr_cagr.reshape(self.n_samples, 1), self.arr_periods
        )
        estimated_matrix = current * arr_cagr_multiplier
        return estimated_matrix


def cagr(start_value, end_value, periods) -> float:
    # Make sure that it can handle negative start or end values.
    cagr = (end_value * 1.0 / start_value) ** (1.0 / periods) - 1
    return cagr


if __name__ == "__main__":
    current_revenue = 2200
    estimated_future_revenue = 1103e9 * 0.5 * 0.05 * 0.689 / 1e6
    ff = forecast_financials(
        **{
            "current_revenue": current_revenue,
            "estimated_future_revenue": estimated_future_revenue,
            "estimated_future_revenue_uncertainty": estimated_future_revenue * 0.25,
            "n_periods": 8,
            "n_shares": 2.11e3,
            "wacc": 0.08,
            "perpetual_rate": 0.015,
            "n_samples": 10000,
            "tax_rate": 0.2,
            "current_gross_margin": 0.039,
            "estimated_gross_margin": 0.2,
            "estimated_gross_margin_uncertainty": 0.03,
            "current_sga_cost": current_revenue * 0.423,
            "estimated_future_sga_cost": estimated_future_revenue * 0.1,
            "estimated_future_sga_cost_uncertainty": estimated_future_revenue * 0.1 * 0,
            "current_dep_amort": current_revenue * 0.1,
            "estimated_future_dep_amort": estimated_future_revenue * 0.1,
            "estimated_future_dep_amort_uncertainty": estimated_future_revenue
            * 0.1
            * 0,
            "current_interest_expense": current_revenue * 0.05,
            "estimated_future_interest_expense": estimated_future_revenue * 0.02,
            "estimated_future_interest_expense_uncertainty": estimated_future_revenue
            * 0.02
            * 0,
            "current_nwc": 1.3,
            "estimated_future_nwc": 6,
            "estimated_future_nwc_uncertainty": 1,
        }
    )
    ff.get_company_value()
