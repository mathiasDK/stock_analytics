import numpy as np


class FinancialForecast:
    # Source of inspiration: https://www.linkedin.com/pulse/how-assess-value-company-combining-discounted-cash-anthony/

    def __init__(
        self,
        current: dict = None,
        estimates: dict | list = None,
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

        scenario_names = []
        total_samples = 0
        for i, estimate in enumerate(self.estimates):
            samples = int(estimate["probability"] * n_samples)
            total_samples += samples
            try:
                scenario_name = estimate["scenario_name"]
            except:
                scenario_name = "scenario_" + str(i)
            for _ in range(samples):
                scenario_names.append(scenario_name)
        self.output = {
            "samples": [
                int(self.n_samples * estimate["probability"])
                for estimate in self.estimates
            ],
            "scenario_name": [
                estimate["scenario_name"]
                if "scenario_name" in estimate.keys()
                else "scenario_" + str(i)
                for i, estimate in enumerate(self.estimates)
            ],
            "scenario_name_long": scenario_names,
        }
        self.n_samples = total_samples

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

        for estimate, samples in zip(self.estimates, self.output["samples"]):
            # For each of the scenarios the estimated revenue matrix must be set and added to the output matrix.
            if (
                not "revenue" in estimate.keys()
                or not "revenue_uncertainty" in estimate.keys()
            ):
                print(
                    "The estimate dictionary must have fields called revenue and revenue_uncertainty."
                )

            # Estimates the revenue matrix and adds it to the output matrix.
            scenario_estimate_revenue_matrix = self._estimated_matrix(
                estimate["revenue"],
                estimate["revenue_uncertainty"],
                self.current["revenue"],
                samples,
            )
            try:
                estimate_revenue_matrix = np.append(
                    estimate_revenue_matrix, scenario_estimate_revenue_matrix, axis=0
                )
            except NameError:
                estimate_revenue_matrix = scenario_estimate_revenue_matrix

        self.output["revenue"] = estimate_revenue_matrix
        return estimate_revenue_matrix

    def get_gross_margin(self) -> np.ndarray:
        if not "gross_margin" in self.current.keys():
            print(
                "The current dictionary must have a field called gross_margin, which should contain the latest known gross_margin."
            )

        for estimate, samples in zip(self.estimates, self.output["samples"]):
            # For each of the scenarios the estimated gross margin matrix must be set and added to the output matrix.
            if (
                not "gross_margin" in estimate.keys()
                or not "gross_margin_uncertainty" in estimate.keys()
            ):
                print(
                    "The estimate dictionary must have fields called gross_margin and gross_margin_uncertainty."
                )

            # Estimates the gross margin matrix and adds it to the output matrix.
            scenario_estimate_gross_margin_matrix = self._estimated_matrix(
                estimate["gross_margin"],
                estimate["gross_margin_uncertainty"],
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

        self.output["gross_margin"] = estimate_gross_margin_matrix
        return estimate_gross_margin_matrix

    def get_gross_profit(self) -> np.ndarray:
        revenue = self.get_revenue()
        gross_margin = self.get_gross_margin()
        gross_profit = revenue * gross_margin
        self.output["gross_profit"] = gross_profit
        return gross_profit

    def get_deprication_amortization(self) -> np.ndarray:
        if not "deprication_amortization" in self.current.keys():
            print(
                "The current dictionary must have a field called deprication_amortization, which should contain the latest known deprication_amortization."
            )

        for estimate, samples in zip(self.estimates, self.output["samples"]):
            # For each of the scenarios the estimated gross margin matrix must be set and added to the output matrix.
            if (
                not "deprication_amortization" in estimate.keys()
                or not "deprication_amortization_uncertainty" in estimate.keys()
            ):
                print(
                    "The estimate dictionary must have fields called deprication_amortization and deprication_amortization_uncertainty."
                )

            # Estimates the gross margin matrix and adds it to the output matrix.
            scenario_estimate_deprication_amortization_matrix = self._estimated_matrix(
                estimate["deprication_amortization"],
                estimate["deprication_amortization_uncertainty"],
                self.current["deprication_amortization"],
                samples,
            )
            try:
                estimate_deprication_amortization_matrix = np.append(
                    estimate_deprication_amortization_matrix,
                    scenario_estimate_deprication_amortization_matrix,
                    axis=0,
                )
            except NameError:
                estimate_deprication_amortization_matrix = (
                    scenario_estimate_deprication_amortization_matrix
                )

        self.output[
            "deprication_amortization"
        ] = estimate_deprication_amortization_matrix
        return estimate_deprication_amortization_matrix

    def get_interest_expense(self) -> np.ndarray:
        if not "interest_expense" in self.current.keys():
            print(
                "The current dictionary must have a field called interest_expense, which should contain the latest known interest_expense."
            )

        for estimate, samples in zip(self.estimates, self.output["samples"]):
            # For each of the scenarios the estimated gross margin matrix must be set and added to the output matrix.
            if (
                not "interest_expense" in estimate.keys()
                or not "interest_expense_uncertainty" in estimate.keys()
            ):
                print(
                    "The estimate dictionary must have fields called interest_expense and interest_expense_uncertainty."
                )

            # Estimates the gross margin matrix and adds it to the output matrix.
            scenario_estimate_interest_expense_matrix = self._estimated_matrix(
                estimate["interest_expense"],
                estimate["interest_expense_uncertainty"],
                self.current["interest_expense"],
                samples,
            )
            try:
                estimate_interest_expense_matrix = np.append(
                    estimate_interest_expense_matrix,
                    scenario_estimate_interest_expense_matrix,
                    axis=0,
                )
            except NameError:
                estimate_interest_expense_matrix = (
                    scenario_estimate_interest_expense_matrix
                )

        self.output["interest_expense"] = estimate_interest_expense_matrix
        return estimate_interest_expense_matrix

    def get_net_working_capital(self) -> np.ndarray:
        if not "net_working_capital" in self.current.keys():
            print(
                "The current dictionary must have a field called net_working_capital, which should contain the latest known net_working_capital."
            )

        for estimate, samples in zip(self.estimates, self.output["samples"]):
            # For each of the scenarios the estimated gross margin matrix must be set and added to the output matrix.
            if (
                not "net_working_capital" in estimate.keys()
                or not "net_working_capital_uncertainty" in estimate.keys()
            ):
                print(
                    "The estimate dictionary must have fields called net_working_capital and net_working_capital_uncertainty."
                )

            # Estimates the gross margin matrix and adds it to the output matrix.
            scenario_estimate_net_working_capital_matrix = self._estimated_matrix(
                estimate["net_working_capital"],
                estimate["net_working_capital_uncertainty"],
                self.current["net_working_capital"],
                samples,
            )
            try:
                estimate_net_working_capital_matrix = np.append(
                    estimate_net_working_capital_matrix,
                    scenario_estimate_net_working_capital_matrix,
                    axis=0,
                )
            except NameError:
                estimate_net_working_capital_matrix = (
                    scenario_estimate_net_working_capital_matrix
                )

        self.output["net_working_capital"] = estimate_net_working_capital_matrix
        return estimate_net_working_capital_matrix

    def get_ebit_margin(self) -> np.ndarray:
        if not "ebit_margin" in self.current.keys():
            print(
                "The current dictionary must have a field called ebit_margin, which should contain the latest known ebit_margin."
            )

        for estimate, samples in zip(self.estimates, self.output["samples"]):
            # For each of the scenarios the estimated gross margin matrix must be set and added to the output matrix.
            if (
                not "ebit_margin" in estimate.keys()
                or not "ebit_margin_uncertainty" in estimate.keys()
            ):
                print(
                    "The estimate dictionary must have fields called ebit_margin and ebit_margin_uncertainty."
                )

            # Estimates the gross margin matrix and adds it to the output matrix.
            scenario_estimate_ebit_margin_matrix = self._estimated_matrix(
                estimate["ebit_margin"],
                estimate["ebit_margin_uncertainty"],
                self.current["ebit_margin"],
                samples,
            )
            try:
                estimate_ebit_margin_matrix = np.append(
                    estimate_ebit_margin_matrix,
                    scenario_estimate_ebit_margin_matrix,
                    axis=0,
                )
            except NameError:
                estimate_ebit_margin_matrix = scenario_estimate_ebit_margin_matrix

        self.output["ebit_margin"] = estimate_ebit_margin_matrix
        return estimate_ebit_margin_matrix

    def get_sga(self) -> np.ndarray:
        if not "gross_profit" in self.output.keys():
            self.get_gross_profit()
        gross_profit = self.output["gross_profit"]
        if not "deprication_amortization" in self.output.keys():
            self.get_deprication_amortization()
        deprication_amortization = self.output["deprication_amortization"]

        if not "ebit_margin" in self.output.keys():
            self.get_ebit_margin()
        ebit_margin = self.output["ebit_margin"]

        sga = gross_profit - deprication_amortization - ebit_margin

        self.output["selling_general_admin_expense"] = sga
        return sga

    def get_net_income(self) -> np.ndarray:
        if not "revenue" in self.output.keys():
            self.get_revenue()
        revenue = self.output["revenue"]
        if not "ebit_margin" in self.output.keys():
            self.get_ebit_margin()
        ebit_margin = self.output["ebit_margin"]
        if not "interest_expense" in self.output.keys():
            self.get_interest_expense()
        interest_expense = self.output["interest_expense"]
        profit_before_tax = revenue * ebit_margin - interest_expense
        tax = profit_before_tax * self.tax_rate
        net_income = profit_before_tax - tax

        self.output["net_income"] = net_income
        return net_income

    def get_free_cashflow(self) -> np.ndarray:

        # Calculating net income
        if not "net_income" in self.output.keys():
            self.get_net_income()
        net_income = self.output["net_income"]

        # Calculating free cash flow
        if not "net_working_capital" in self.output.keys():
            self.get_net_working_capital()
        nwc = self.output["net_working_capital"]
        if not "interest_expense" in self.output.keys():
            self.get_interest_expense()
        int_exp = self.output["interest_expense"]
        if not "deprication_amortization" in self.output.keys():
            self.get_deprication_amortization()
        dep_amort = self.output["deprication_amortization"]
        capex = dep_amort  # WHY?
        fcf = net_income - int_exp - dep_amort + nwc + capex

        self.output["free_cashflow"] = fcf
        return fcf

    def get_discount_factor(self) -> np.ndarray:
        arr_periods = np.ones((self.n_samples, self.n_periods)) * np.linspace(
            1, self.n_periods, self.n_periods
        )
        discount_factor = np.power(1 + self.wacc, arr_periods)
        return discount_factor

    def get_discounted_company_value(self) -> np.ndarray:
        if not "free_cashflow" in self.output.keys():
            self.get_free_cashflow()
        fcf = self.output["free_cashflow"]
        discount_factor = self.get_discount_factor()
        npv = fcf / discount_factor

        terminal_value = (
            fcf[:, -1]
            * (1 + self.perpetual_rate)
            / (self.wacc - self.perpetual_rate)
            / discount_factor[:, -1]
        )

        company_value = np.sum(npv, axis=1) + terminal_value

        self.output["company_value"] = company_value
        return company_value

    def get_fair_value_per_share(self) -> np.array:
        if not "company_value" in self.output.keys():
            self.get_discounted_company_value()

        shares_full = []

        # Adding the number of shares for each scenario so it can divide the discounted
        # company value and thereby calculate the current value of the shares.
        for estimate, samples in zip(self.estimates, self.output["samples"]):

            # shares = [estimate['shares']]*samples
            [shares_full.append(estimate["shares"]) for _ in range(samples)]
            # shares_full = [item for sublist in shares_full for item in sublist]  # Flattening

        fair_value_per_share = self.output["company_value"] / np.array(shares_full)
        self.output["fair_value_per_share"] = fair_value_per_share
        return fair_value_per_share

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
    current = {
        "revenue": 2200,
        "gross_margin": 0.2,
        "ebit_margin": 0.1,
        "interest_expense": 100,
        "deprication_amortization": 200,
        "net_working_capital": 100,
    }

    scenario_1 = {
        "revenue": 3500,
        "revenue_uncertainty": 200,
        "gross_margin": 0.25,
        "gross_margin_uncertainty": 0.05,
        "deprication_amortization": 200,
        "deprication_amortization_uncertainty": 200,
        "interest_expense": 200,
        "interest_expense_uncertainty": 10,
        "net_working_capital": 100,
        "net_working_capital_uncertainty": 0,
        "ebit_margin": 0.15,
        "ebit_margin_uncertainty": 0.02,
        "probability": 0.75,
        "scenario_name": "random",
        "shares": 10000,
    }
    scenario_2 = {
        "revenue": 3500,
        "revenue_uncertainty": 200,
        "gross_margin": 0.35,
        "gross_margin_uncertainty": 0.05,
        "deprication_amortization": 200,
        "deprication_amortization_uncertainty": 200,
        "interest_expense": 200,
        "interest_expense_uncertainty": 10,
        "net_working_capital": 100,
        "net_working_capital_uncertainty": 0,
        "ebit_margin": 0.25,
        "ebit_margin_uncertainty": 0.02,
        "probability": 0.25,
        "scenario_name": "likely",
        "shares": 10000,
    }
    estimates = [scenario_1, scenario_2]
    ff = FinancialForecast(
        current,
        estimates,
        n_periods=5,
        n_samples=10,
        tax_rate=0.22,
        wacc=0.08,
        perpetual_rate=0.02,
    )
    ff.get_ebit_margin()
    ff.get_fair_value_per_share()
