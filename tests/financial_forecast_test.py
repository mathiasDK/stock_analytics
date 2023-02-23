import unittest
from src.financial_forecast.forecast_financials import cagr


class TestGrowthMethods(unittest.TestCase):
    def test_constant_growth(self):
        self.assertEqual(cagr(1, 4, 2), 1)


if __name__ == "__main__":
    unittest.main()
