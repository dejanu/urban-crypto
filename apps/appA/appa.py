#!/usr/bin/env python

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/price"
CRYPTOCOMPARE_PARAMS = {"fsym": "BTC", "tsyms": "USD"}


def get_btc_value():
    """
    update btc_values dict
    """
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL, params=CRYPTOCOMPARE_PARAMS)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        app.config['bitcoin_value'] = data
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Schedule the job to fetch Bitcoin value every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(get_btc_value, 'interval', seconds=5)
scheduler.start()
# Fetch Bitcoin value initially
get_btc_value()

@app.route('/')
def index():
    """
    home page
    """
    return '<p><b> Service endpoints /now and /tensec </p></b>'

@app.route('/now')
def get_now():
    """
    Current value of Bitcoin in USD
    """
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL, params=CRYPTOCOMPARE_PARAMS)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route('/tensec')
def get_tensec():
    """
    Value of Bitcoin updated every 10 seconds
    """
    # get the last key from dict btc_values btc_values[list(btc_values.keys())[-1]]
    bitcoin_value = app.config.get('bitcoin_value')
    if bitcoin_value:
        return jsonify(bitcoin_value)
    else:
        return "Bitcoin value not available at the moment"
 
if __name__ == "__main__":
    app.run(debug=True)
