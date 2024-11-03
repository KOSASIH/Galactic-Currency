# tests/e2e/test_application.py

import pytest
import requests

class TestApplication:
    BASE_EXCHANGE_URL = 'http://localhost:5002/exchange'
    BASE_NOTIFICATION_URL = 'http://localhost:5003/notify'

    def test_full_exchange_and_notification_flow(self):
        # Step 1: Perform a currency exchange
        exchange_response = requests.get(self.BASE_EXCHANGE_URL, params={
            'from': 'USD',
            'to': 'EUR',
            'amount': 100
        })
        assert exchange_response.status_code == 200
        exchange_data = exchange_response.json()
        assert 'converted_amount' in exchange_data
        converted_amount = exchange_data['converted_amount']

        # Step 2: Send a notification about the exchange
        notification_response = requests.post(self.BASE_NOTIFICATION_URL, json={
            'type': 'email',
            'recipient': 'test@example.com',
            'message': f'Converted 100 USD to {converted_amount} EUR.'
        })
        assert notification_response.status_code == 200
        notification_data = notification_response.json()
        assert 'status' in notification_data

    def test_invalid_currency_exchange(self):
        # Attempt to exchange with an invalid currency
        response = requests.get(self.BASE_EXCHANGE_URL, params={
            'from': 'USD',
            'to': 'INVALID',
            'amount': 100
        })
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data

    def test_notification_with_invalid_type(self):
        # Attempt to send a notification with an invalid type
        response = requests.post(self.BASE_NOTIFICATION_URL, json={
            'type': 'invalid_type',
            'recipient': 'test@example.com',
            'message': 'This should fail.'
        })
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data

if __name__ == '__main__':
    pytest.main()
