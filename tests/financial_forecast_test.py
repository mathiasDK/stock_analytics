import unittest
from src.financial_forecast.forecast_financials import cagr, ForecastFinancial


class TestGrowthMethods(unittest.TestCase):
    def test_constant_growth(self):
        self.assertEqual(cagr(1, 4, 2), 1)

class TestForecast(unittest.TestCase):
    def test_revenue_size(self):
        ff=ForecastFinancial(current_revenue=10, n_periods=5)
        rev = ff.get_revenue(best_case=50, middle_case=25, worst_case=10, uncertainty=0.02)
        self.assertEqual(rev.shape, ff.arr_periods.shape)


if __name__ == "__main__":
    unittest.main()
