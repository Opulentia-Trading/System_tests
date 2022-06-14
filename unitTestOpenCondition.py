import unittest
#from fcntl import F_SEAL_SEAL
import json
from math import ceil
import requests
from matplotlib import pyplot as plt, dates as mdates
from datetime import datetime

from test_data.open_position_data import open_data

class Validator(unittest.TestCase):
    # def __init__(self):
    #    pass

    def validate(self, funding_rate, spot_price, futures_price, platform_asset):
        number_needed_funding_cycles = self.check_fees(funding_rate)
        if number_needed_funding_cycles >= 35:
            return False
        
        percent_price_gap = self.check_price_gap(spot_price, futures_price)
        if abs(percent_price_gap) < 1:
            return False

        if funding_rate > 0:
            return True
        else:
            return True

    def check_fees(self, funding_rate):
        binance_spot_fee_percentage = 0.1
        binance_futures_fee_percentage = 0.04
        fee_percentage = (2 * binance_spot_fee_percentage) + (2 * binance_futures_fee_percentage)

        number_needed_funding_cycles = ceil(fee_percentage/funding_rate)

        return number_needed_funding_cycles

    def check_price_gap(self, spot_price, futures_price):
        percent_price_gap = ((futures_price - spot_price) / spot_price) * 100

        return percent_price_gap

    # Note: This test is aborted for now as using an API for test data eliminates
    # the test's ability to be repeatable
    # def test_open(self):
    #     url = "https://fapi.binance.com/fapi/v1/fundingRate"

    #     payload = {
    #         "symbol": "BTCUSDT",
    #         # "startTime": 1000,
    #         # "endTime": 1010,
    #         "limit": 500
    #     }

    #     res = requests.get(url, params=payload)

    #     for elem in res.json():
    #         with self.subTest(funding_rate=elem['fundingRate'], spot_price=100, futures_price=105, platform_asset=elem['symbol']):
    #             self.assertEqual(self.validate(funding_rate=float(elem['fundingRate']), spot_price=100, futures_price=105, platform_asset=elem['symbol']), True)


    def test_open_v2(self):
        for elem in open_data:
            with self.subTest(index=elem['index'], funding_rate=elem['funding_rate'], spot_price=elem['spot_price'], futures_price=elem['futures_price'], platform_asset=elem['platform_asset']):
                self.assertEqual(self.validate(funding_rate=float(elem['funding_rate']), spot_price=elem['spot_price'], futures_price=elem['futures_price'], platform_asset=elem['platform_asset']), elem['result'])


# To run all tests:
# python3 -m unittest unitTestOpenCondition

# To run specific (Validator) class:
# python3 -m unittest unitTestOpenCondition.Validator

# To run specific (test_open_v2) test:
# python3 -m unittest unitTestOpenCondition.Validator.test_open_v2

if __name__ == '__main__':
    unittest.main()