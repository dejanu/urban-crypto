#!/usr/bin/env python

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock

import requests

from collections import deque
from datetime import datetime, timedelta

app = Flask(__name__)

CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/price"
CRYPTOCOMPARE_PARAMS = {"fsym": "BTC", "tsyms": "USD"}

bitcoin_values = deque(maxlen=60) # store for BTC, deque with (timestamp:btc_value)

# create scheduler
scheduler = BackgroundScheduler()
# create Lock for the thread that executes the job
fetch_lock = Lock()

def get_btc_value():
    """
    get btc value
    """
    # try to aquire the lock 
    if fetch_lock.acquire(blocking=False):
        try:
            response = requests.get(CRYPTOCOMPARE_API_URL, params=CRYPTOCOMPARE_PARAMS)
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
 
            bitcoin_values.append((datetime.now(), response.json()['USD'])) # dict in response  {'USD': 71000.64}
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        finally:
            # release the lock to allow subsequent executions
            fetch_lock.release()
    else:
        print(" Previous execution is still in progress.")

# Schedule the job to fetch Bitcoin value every 10 seconds
scheduler.add_job(get_btc_value, 'interval', seconds=10)
scheduler.start()

# Fetch Bitcoin value initially
get_btc_value()

@app.route('/')
def index():
    """
    Value of Bitcoin updated every 10 seconds
    """
    #return "<p><hr><center>BTC value:{0}</p></center>".format(app.config.get('bitcoin_values','No BTC value available at the moment'))
    print(bitcoin_values)
    return "<p><hr><center>BTC USD value:{0}</p></center>".format(bitcoin_values[-1][1])

@app.route('/avg')
def avg():
    """
    Value of Bitcoin average over 10 min
    """
    delta = datetime.now() - timedelta(minutes=1)
    recent_data = []
    print(delta, datetime.now())

    for data in bitcoin_values:
        print(data[0])
        if data[0] >= delta:
            recent_data.append(data[1])
    print(recent_data)        
    # Calculate average value
    if recent_data:
        average_value = sum(recent_data) / len(recent_data)
        return jsonify({"Average BTC USD value (last 1 min)": average_value})
    else:
        return jsonify({"message": "No BTC value available in the last 1 minutes"})

@app.route('/now')
def get_now():
    """
    Current value of Bitcoin in USD
    """
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL, params=CRYPTOCOMPARE_PARAMS)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return "<p><hr><center>BTC current value:{0}</p></center>".format(data)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5555)
