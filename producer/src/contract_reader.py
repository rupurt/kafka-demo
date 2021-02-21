from event_publisher import Publisher
import os
import json
import time
import logging
# this is it! To be sure about which AnswerUpdated to fetch I need to make sure
# that latestData[1] == Web3.toJSON(event).get('args').get('current')
import asyncio
from web3 import Web3
from configparser import ConfigParser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


config = ConfigParser()
config.read('config.ini')

# inject infura project id from ENV
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{os.getenv('INFURA_PROJECT_ID', 'ENV VARIABLE INFURA_PROJECT_ID NOT FOUND!')}",
                            request_kwargs={'timeout': 10}))

publisher = Publisher()


class ContractHook:

    def __init__(self, topic: str, poll_interval: int = 2):
        """

        :param topic:
        """
        self.topic = topic
        self.poll_interval = poll_interval

    def handle_event(self, event: str, event_type: str):
        """
        Transform event
        :param event_type:
        :param event:
        :return:
        """
        event = Web3.toJSON(event)
        event = json.loads(event)
        event['event_type'] = event_type
        # print(f"in handle event {event}")

        publisher.push(json.dumps(event), topic=self.topic)

    async def log_loop(self, event_filter: str, event_type: str):
        """
        Listen to events
        :param event_filter:
        :param poll_interval:
        :param event_type:
        :return:
        """
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event, event_type)
            await asyncio.sleep(self.poll_interval)

    async def run(self):
        """

        :return:
        """
        # block_filter = web3.eth.filter('latest')
        # tx_filter = web3.eth.filter('pending')
        tasks = []
        for section in config.sections():
            contract = w3.eth.contract(address=config.items(section)[1][1], abi=config.items(section)[0][1])
            event_filter = contract.events.AnswerUpdated.createFilter(fromBlock='latest')

            tasks.append(asyncio.create_task(self.log_loop(event_filter, section)))

        await asyncio.gather(*tasks)

