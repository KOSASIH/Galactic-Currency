# tests/integration/test_exchange_service.py

import unittest
import requests

class TestExchangeService(unittest.TestCase):
    BASE_URL = 'http://localhost:5002/exchange'

    def test_exchange_usd_to_eur(self):
        response = requests.get(self.BASE_URL, params={'from': 'USD', 'to': 'EUR', 'amount': 100})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('converted_amount', data)

    def test_exchange_invalid_currency(self):
        response = requests.get(self.BASE_URL, params={'from': 'USD', 'to': 'INVALID', 'amount': 100})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
