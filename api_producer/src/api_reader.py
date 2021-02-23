from event_publisher import Publisher
import json
from typing import Dict
import logging
import requests

# to test I can use a test topic and call producer.send

# ideas: make a transform method that parses the response into a standardized format to be pushed to the topic
# TODO: for both endpoints I need to first get the coin id's from the tickers (both have a list of coins)
# TODO: however this call needs to be made only once and can be cached, so best would be in the class constructor
# write some tests that mock the API's response
# polling the API's is the only possibility, since no ws or webhooks
# topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'


publisher = Publisher()


class APIHook:
    """
    Abstracts the API call
    """
    def __init__(self, topic: str):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = logger
        # topic is actually static...
        self.topic = topic

    def get_coinlists(self):
        # initial call that gets the tickers from
        # the coin id or the "base" and "vs"
        pass

    def fetch(self,  base_url: str, params: Dict, event_type: str, timeout=5):
        """

        :param event_type:
        :param timeout:
        :param params:
        :param base_url:
        :return:
        """
        try:
            resp = requests.get(base_url, params=params, timeout=timeout)
        except requests.exceptions.ReadTimeout as e:
            self.logger.warning(e)
        self.logger.info(f"Fetched: {resp.json()}")
        resp = self._transform(resp.json(), event_type)
        self.publish(resp)

    def fetch_custom(self, base_url: str, event_type: str, params: str = '', timeout=5):
        """

        :param event_type:
        :param timeout:
        :param params:
        :param base_url:
        :return:
        """
        url = base_url + params
        try:
            resp = requests.get(url, timeout=timeout)
        except requests.exceptions.ReadTimeout as e:
            self.logger.warning(e)

        self.logger.info(f"Fetched: {resp.json()}")
        resp = self._transform(resp.json(), event_type)
        self.publish(resp)

    def publish(self, msg):
        publisher.push(msg, self.topic)

    def _transform(self, response, event_type):
        if isinstance(response, list):
            response = response[0]
        response['event_type'] = event_type
        return response

