from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import os
import time
import logging
import requests

#ideas: make a transform method that parses the response into a standardized format to be pushed to the topic
# for both endpoints I need to first get the coin id's from the tickers (both have a list of coins)
# write some tests that mock the API's response
# polling the API's is the only possibility, since no ws or webhooks
# topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'
topic = 'stats'


coin_id = "btc-bitcoin"
coinpaprika_url = f"https://api.coinpaprika.com/v1/coins/{coin_id}/ohlcv/today"

base = "ethereum,bitcoin,chainlink"
vs = "usd"
coingecko_url = "https://api.coingecko.com/api/v3/simple/price" #?ids=ethereum&vs_currencies=usd"


class Publisher:

    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = logger

        while not hasattr(self, 'producer'):
            try:
                self.producer = KafkaProducer(bootstrap_servers="kafka:9092")
            except NoBrokersAvailable as err:
                self.logger.error("Unable to find a broker: {0}".format(err))
                time.sleep(1)

    def get_prices(self):
        params = {
            'ids': base,
            'vs_currencies': vs

        }
        resp = requests.get(coingecko_url, params=params)

        self.logger.info(f"Fetched: {resp.json()}")
        self.push(resp.json())

    def push(self, message):
        self.logger.info(f"Publishing: {message}")
        try:
            if self.producer:
                self.producer.send(topic,
                                   bytes(json.dumps(message).encode('utf-8')))
        except AttributeError:
            self.logger.error(f"Unable to send {message}. The producer does not exist.")

    def run(self):
        while True:
            self.logger.info("Calling API")
            self.get_prices()
            time.sleep(20)

    def transform(self):
        pass

