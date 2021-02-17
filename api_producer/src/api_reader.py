from event_publisher import Publisher
import json
import os
import time
import logging
import requests

# to test I can use a test topic and call producer.send

# ideas: make a transform method that parses the response into a standardized format to be pushed to the topic
# for both endpoints I need to first get the coin id's from the tickers (both have a list of coins)
# write some tests that mock the API's response
# polling the API's is the only possibility, since no ws or webhooks
# topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'

coin_id = "btc-bitcoin"
coinpaprika_url = f"https://api.coinpaprika.com/v1/coins/{coin_id}/ohlcv/today"

base = "ethereum,bitcoin,chainlink"
vs = "usd"
coingecko_url = "https://api.coingecko.com/api/v3/simple/price" #?ids=ethereum&vs_currencies=usd"

publisher = Publisher()


class APIHook:

    def __init__(self, topic):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = logger
        self.topic = topic

    # this can be part of a FETCH_FROM_API class, i.e. separate API stuff from publisher
    # make aprams an argument
    def get_prices(self):
        params = {
            'ids': base,
            'vs_currencies': vs

        }
        resp = requests.get(coingecko_url, params=params)
        self.logger.info(f"Fetched: {resp.json()}")
        publisher.push(resp.json(), self.topic)

    def run(self):
        while True:
            self.logger.info("Calling API")
            self.get_prices()
            time.sleep(15)

    def transform(self):
        pass

