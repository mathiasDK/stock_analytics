import unittest
from src.financial_forecast.forecast_financials import cagr, ForecastFinancial


class TestGrowthMethods(unittest.TestCase):
    def test_constant_growth(self):
        self.assertEqual(cagr(1, 4, 2), 1)

class TestForecast(unittest.TestCase):
    def test_revenue_size(self):
        current = {
            'revenue': 10
        }
        scenario_1 = {
            'revenue': 20,
            'revenue_uncertainty': 2,
            'probability': 0.8
        }
        scenario_2 = {
            'revenue': 30,
            'revenue_uncertainty': 3,
            'probability': 0.2
        }
        estimates = [scenario_1, scenario_2]
        ff=ForecastFinancial(current=current, estimates=estimates, n_samples=10000, n_periods=5)
        rev = ff.get_revenue()
        self.assertEqual(rev.shape, (ff.n_samples, ff.n_periods))


if __name__ == "__main__":
    unittest.main()
