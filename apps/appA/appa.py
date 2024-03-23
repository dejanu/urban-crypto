#!/usr/bin/env python
from flask import Flask, jsonify
import requests

app = Flask(__name__)

CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/price"
CRYPTOCOMPARE_PARAMS = {"fsym": "BTC", "tsyms": "USD"}

@app.route('/')
def index():
    """
    home page
    """
    return '<p><b> Service endpoints /now and /avg </p></b>'

@app.route('/now')
def get_now():
    try:
        response =  requests.get(CRYPTOCOMPARE_API_URL, params=CRYPTOCOMPARE_PARAMS)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
