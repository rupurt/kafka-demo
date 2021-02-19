from event_publisher import Publisher
import json
import os
import time
import logging
import requests

# to test I can use a test topic and call producer.send

# ideas: make a transform method that parses the response into a standardized format to be pushed to the topic
# TODO: for both endpoints I need to first get the coin id's from the tickers (both have a list of coins)
# TODO: however this call needs to be made only once and can be cached, so best would be in the class constructor
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
    """
    Abstracts the API call
    """
    def __init__(self, topic):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = logger
        # topic is actually static...
        self.topic = topic

    def get_coinlists(self):
        # here I can make the initial call that gets the tickers from
        # the coin id or the "base" and "vs"
        # or maybe move it to another class
        pass

    def get_prices(self):
        """

        :return:
        """
        params = {
            'ids': base,
            'vs_currencies': vs

        }
        resp = requests.get(coingecko_url, params=params)
        self.logger.info(f"Fetched: {resp.json()}")
        self.publish(resp)

    def publish(self, msg):
        publisher.push(msg.json(), self.topic)

    # maybe move this to the main file
    # so I can wrap all the calls in a loop
    def run(self):
        while True:
            self.logger.info("Calling API")
            self.get_prices()
            time.sleep(15)

    def transform(self):
        pass

