# services/exchange_service.py

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

class ExchangeService:
    def __init__(self):
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"  # Example API
        self.rates = self.fetch_exchange_rates()

    def fetch_exchange_rates(self):
        """Fetch the latest exchange rates from an external API."""
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json().get('rates', {})
        else:
            raise Exception("Failed to fetch exchange rates")

    def convert_currency(self, from_currency, to_currency, amount):
        """Convert an amount from one currency to another."""
        if from_currency == "USD":
            rate = self.rates.get(to_currency)
            if rate:
                return amount * rate
            else:
                raise ValueError("Invalid target currency")
        else:
            # Convert from the specified currency to USD first
            usd_amount = amount / self.rates.get(from_currency)
            return usd_amount * self.rates.get(to_currency)

exchange_service = ExchangeService()

@app.route('/exchange', methods=['GET'])
def exchange():
    """API endpoint to convert currencies."""
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = float(request.args.get('amount'))

    try:
        converted_amount = exchange_service.convert_currency(from_currency, to_currency, amount)
        return jsonify({
            'from': from_currency,
            'to': to_currency,
            'amount': amount,
            'converted_amount': converted_amount
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5002)
