import numpy as np


class ForecastFinancial:
    # Source of inspiration: https://www.linkedin.com/pulse/how-assess-value-company-combining-discounted-cash-anthony/

    def __init__(
        self,
        current: dict = None,
        estimates=None,
        # current_revenue=None,
        # estimated_future_revenue=None,
        # estimated_future_revenue_uncertainty=None,
        # current_gross_margin=None,
        # estimated_gross_margin=None,
        # estimated_gross_margin_uncertainty=None,
        # current_sga_cost=None,
        # estimated_future_sga_cost=None,
        # estimated_future_sga_cost_uncertainty=None,
        # current_dep_amort=None,
        # estimated_future_dep_amort=None,
        # estimated_future_dep_amort_uncertainty=None,
        # current_interest_expense=None,
        # estimated_future_interest_expense=None,
        # estimated_future_interest_expense_uncertainty=None,
        # current_nwc=None,
        # estimated_future_nwc=None,
        # estimated_future_nwc_uncertainty=None,
        n_periods=None,
        n_shares=None,
        wacc=None,
        perpetual_rate=None,
        n_samples=10000,
        tax_rate=None,
        **kwargs
    ) -> None:
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

        self.current = current
        if isinstance(estimates, dict):
            self.estimates = [estimates]
        elif isinstance(estimates, list):
            self.estimates = estimates
        # self.current_revenue=current_revenue
        # self.estimated_future_revenue=estimated_future_revenue
        # self.estimated_future_revenue_uncertainty=estimated_future_revenue_uncertainty
        # self.current_gross_margin=current_gross_margin
        # self.estimated_gross_margin=estimated_gross_margin
        # self.estimated_gross_margin_uncertainty=estimated_gross_margin_uncertainty
        # self.current_sga_cost=current_sga_cost
        # self.estimated_future_sga_cost=estimated_future_sga_cost
        # self.estimated_future_sga_cost_uncertainty=estimated_future_sga_cost_uncertainty
        # self.current_dep_amort=current_dep_amort
        # self.estimated_future_dep_amort=estimated_future_dep_amort
        # self.estimated_future_dep_amort_uncertainty=estimated_future_dep_amort_uncertainty
        # self.current_interest_expense=current_interest_expense
        # self.estimated_future_interest_expense=estimated_future_interest_expense
        # self.estimated_future_interest_expense_uncertainty=estimated_future_interest_expense_uncertainty
        # self.current_nwc=current_nwc
        # self.estimated_future_nwc=estimated_future_nwc
        # self.estimated_future_nwc_uncertainty=estimated_future_nwc_uncertainty
        self.n_periods = n_periods
        self.wacc = wacc
        self.perpetual_rate = perpetual_rate
        self.n_samples = n_samples
        self.tax_rate = tax_rate

    def get_revenue(self) -> np.ndarray:
        """Create a matrix with a shape of n_samples*n_periods with the estimated revenue in each period for each simulation.
        Each simulation has a CAGR and that CAGR is used for the growth rate of revenue.

        Raises:
            Exception: If the estimated_future_revenue haven't been set through the set_revenue() function, then it will raise an error.

        Returns:
            np.ndarray: An array with shape n_samples*n_periods with the estimated revenue in each period for each simulation.
        """

        if not "revenue" in self.current.keys():
            print(
                "The current dictionary must have a field called revenue, which should contain the latest known revenue."
            )

        samples_total = 0

        for estimate_dict in self.estimates:
            # For each of the scenarios the estimated revenue matrix must be set and added to the output matrix.
            if (
                not "revenue" in estimate_dict.keys()
                or not "revenue_uncertainty" in estimate_dict.keys()
                or not "probability" in estimate_dict.keys()
            ):
                print(
                    "The estimate dictionary must have fields called revenue and revenue_uncertainty."
                )

            # Making sure that the sample size is correct.
            if estimate_dict == self.estimates[-1]:
                samples = int(self.n_samples - samples_total)
            else:
                samples = int(self.n_samples * estimate_dict["probability"])
                samples_total += samples

            # Estimates the revenue matrix and adds it to the output matrix.
            scenario_estimate_revenue_matrix = self._estimated_matrix(
                estimate_dict["revenue"],
                estimate_dict["revenue_uncertainty"],
                self.current["revenue"],
                samples,
            )
            try:
                estimate_revenue_matrix = np.append(
                    estimate_revenue_matrix, scenario_estimate_revenue_matrix, axis=0
                )
            except NameError:
                estimate_revenue_matrix = scenario_estimate_revenue_matrix

        return estimate_revenue_matrix

    def get_gross_margin(self) -> np.ndarray:
        if not "gross_margin" in self.current.keys():
            print(
                "The current dictionary must have a field called gross_margin, which should contain the latest known gross_margin."
            )

        samples_total = 0

        for estimate_dict in self.estimates:
            # For each of the scenarios the estimated gross margin matrix must be set and added to the output matrix.
            if (
                not "gross_margin" in estimate_dict.keys()
                or not "gross_margin_uncertainty" in estimate_dict.keys()
                or not "probability" in estimate_dict.keys()
            ):
                print(
                    "The estimate dictionary must have fields called gross_margin and gross_margin_uncertainty."
                )

            # Making sure that the sample size is correct.
            if estimate_dict == self.estimates[-1]:
                samples = int(self.n_samples - samples_total)
            else:
                samples = int(self.n_samples * estimate_dict["probability"])
                samples_total += samples

            # Estimates the gross margin matrix and adds it to the output matrix.
            scenario_estimate_gross_margin_matrix = self._estimated_matrix(
                estimate_dict["gross_margin"],
                estimate_dict["gross_margin_uncertainty"],
                self.current["gross_margin"],
                samples,
            )
            try:
                estimate_gross_margin_matrix = np.append(
                    estimate_gross_margin_matrix,
                    scenario_estimate_gross_margin_matrix,
                    axis=0,
                )
            except NameError:
                estimate_gross_margin_matrix = scenario_estimate_gross_margin_matrix

        return estimate_gross_margin_matrix

    def get_gross_profit(self) -> np.ndarray:
        revenue = self.get_revenue()
        gross_margin = self.get_gross_margin()
        gross_profit = revenue * gross_margin
        return gross_profit

    def get_sga(self) -> np.ndarray:
        pass

    def get_dep_amort(self) -> np.ndarray:
        pass

    def get_interest_expense(self) -> np.ndarray:
        pass

    def get_nwc(self) -> np.ndarray:
        pass

    def get_ebit_margin(self) -> np.ndarray:
        if not "ebit_margin" in self.current.keys():
            print(
                "The current dictionary must have a field called ebit_margin, which should contain the latest known ebit_margin."
            )

        samples_total = 0

        for estimate_dict in self.estimates:
            # For each of the scenarios the estimated gross margin matrix must be set and added to the output matrix.
            if (
                not "ebit_margin" in estimate_dict.keys()
                or not "ebit_margin_uncertainty" in estimate_dict.keys()
                or not "probability" in estimate_dict.keys()
            ):
                print(
                    "The estimate dictionary must have fields called ebit_margin and ebit_margin_uncertainty."
                )

            # Making sure that the sample size is correct.
            if estimate_dict == self.estimates[-1]:
                samples = int(self.n_samples - samples_total)
            else:
                samples = int(self.n_samples * estimate_dict["probability"])
                samples_total += samples

            # Estimates the gross margin matrix and adds it to the output matrix.
            scenario_estimate_ebit_margin_matrix = self._estimated_matrix(
                estimate_dict["ebit_margin"],
                estimate_dict["ebit_margin_uncertainty"],
                self.current["ebit_margin"],
                samples,
            )
            try:
                estimate_gross_margin_matrix = np.append(
                    estimate_gross_margin_matrix,
                    scenario_estimate_ebit_margin_matrix,
                    axis=0,
                )
            except NameError:
                estimate_ebit_margin_matrix = scenario_estimate_ebit_margin_matrix

        return estimate_ebit_margin_matrix

    def get_net_income(self) -> np.ndarray:
        # gross_profit = self.get_gross_profit()
        # sga = -1 * self.get_sga()
        # dep_amort = self.get_dep_amort()
        # int_exp = self.get_interest_expense()
        revenue = self.get_revenue()
        ebit_margin = self.get_ebit_margin()
        profit_before_tax = revenue * ebit_margin  # gross_profit + sga + dep_amort + int_exp
        tax = profit_before_tax * self.tax_rate * -1.0
        net_income = profit_before_tax + tax
        return net_income

    def get_fcf(self) -> np.ndarray:

        # Calculating net income
        net_income = self.get_net_income()

        # Calculating free cash flow
        nwc = self.get_nwc()
        int_exp = self.get_interest_expense()
        dep_amort = self.get_dep_amort()
        capex = dep_amort  # WHY?
        fcf = net_income - int_exp - dep_amort + nwc + capex
        return fcf

    def get_discount_factor(self) -> np.ndarray:
        discount_factor = np.power(1 + self.wacc, self.arr_periods)
        return discount_factor

    def get_discounted_company_value(self) -> np.ndarray:
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
        self.discounted_company_value = company_value
        return company_value

    def get_fair_value_per_share(self) -> np.array:
        if not hasattr(self, "discounted_company_value"):
            # Making sure that there is a discounted company value calculated
            self.get_discounted_company_value()

        samples_total = 0
        shares_full = []

        # Adding the number of shares for each scenario so it can divide the discounted 
        # company value and thereby calculate the current value of the shares.
        for estimate_dict in self.estimates:
            if estimate_dict == self.estimates[-1]:
                samples = int(self.n_samples - samples_total)
            else:
                samples = int(self.n_samples * estimate_dict["probability"])
                samples_total += samples

            shares = [estimate_dict['shares']]*samples
            shares_full.append(shares)
            shares_full = [item for sublist in shares_full for item in sublist]  # Flattening

        return self.discounted_company_value / np.array(shares_full)

    def _estimated_matrix(self, estimate, uncertainty, current, samples):
        arr_periods = np.ones((samples, self.n_periods)) * np.linspace(
            1, self.n_periods, self.n_periods
        )

        arr_estimate = np.random.normal(estimate, uncertainty, samples)
        arr_cagr = cagr(current, arr_estimate, self.n_periods)
        arr_cagr_multiplier = np.power(1 + arr_cagr.reshape(samples, 1), arr_periods)
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
