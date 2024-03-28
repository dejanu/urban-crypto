#!/usr/bin/env python

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/price"
CRYPTOCOMPARE_PARAMS = {"fsym": "BTC", "tsyms": "USD"}

def get_btc_value():
    """
    get btc value
    """
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL, params=CRYPTOCOMPARE_PARAMS)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        app.config['bitcoin_value'] = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Schedule the job to fetch Bitcoin value every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(get_btc_value, 'interval', seconds=10)
scheduler.start()
# Fetch Bitcoin value initially
get_btc_value()

@app.route('/')
def index():
    """
    Value of Bitcoin updated every 10 seconds
    """
    # get the last key from dict btc_values btc_values[list(btc_values.keys())[-1]]
    bitcoin_value = app.config.get('bitcoin_value')
    if bitcoin_value:
        return "<p><hr><center>BTC value:{0}</p></center>".format(bitcoin_value)
    else:
        return "Bitcoin value not available at the moment, for instant value check /now endpoint"

@app.route('/now')
def get_now():
    """
    Current value of Bitcoin in USD
    """
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL, params=CRYPTOCOMPARE_PARAMS)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return "<p><hr><center>BTC currentvalue:{0}</p></center>".format(data)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
