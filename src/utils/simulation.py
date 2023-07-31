import numpy as np

class MonteCarloSimulation:
    def __init__(self, kpi_current: float, kpi_estimated: float, kpi_std: float, financial_current: float, financial_estimated: float, financial_std: float) -> None:
        self.kpi_current = kpi_current
        self.kpi_estimated = kpi_estimated
        self.kpi_std = kpi_std
        self.financial_current = financial_current
        self.financial_estimated = financial_estimated
        self.financial_std = financial_std
        self.n_simulations = 100000

    def get_kpi_distribution(self) -> np.ndarray:
        dist_estimated = np.random.normal(self.kpi_estimated, self.kpi_std, size = self.n_simulations)
        return dist_estimated

    def get_financial_distribution(self) -> np.ndarray:
        dist_estimated = np.random.normal(self.financial_estimated, self.financial_std, size = self.n_simulations)
        return dist_estimated

    def get_valuation_distribution(self) -> np.ndarray:
        dist_valuation = self.get_kpi_distribution() * self.get_financial_distribution()
        return dist_valuation
    
    def get_valuation_cagr_distribution(self, periods: float) -> np.ndarray:
        valuation_current = self.kpi_current * self.financial_current
        estimated_valuation = self.get_valuation_distribution()
        if min(estimated_valuation)<0:
            print("It is not possible to calculate a cagr to a negative ending value")
            return None
        else:
            cagr = (estimated_valuation / valuation_current)**(1/periods) - 1
            return cagr
        
if __name__ == "__main__":
    d = {
        "kpi_current": 15,
        "kpi_estimated": 20,
        "kpi_std": 1,
        "financial_current": 200,
        "financial_estimated": 280,
        "financial_std": 30,
    }
    MC = MonteCarloSimulation(**d)
    print(MC.get_valuation_cagr_distribution(periods=5))