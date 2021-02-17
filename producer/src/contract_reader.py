from event_publisher import Publisher
import os
import json
import time
import logging
# this is it! To be sure about which AnswerUpdated to fetch I need to make sure
# that latestData[1] == Web3.toJSON(event).get('args').get('current')
import asyncio
from web3 import Web3

# INJECT INFURA PROJECT ID FROM ENV
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{os.getenv('INFURA_PROJECT_ID', 'ENV VARIABLE INFURA_PROJECT_ID NOT FOUND!')}",
                            request_kwargs={'timeout': 10}))


publisher = Publisher()


class ContractHook:

    def __init__(self, address: str, abi: str, topic: str):
        """

        :param address:
        :param abi:
        :param topic:
        """
        self.contract = w3.eth.contract(address=address, abi=abi)
        self.topic = topic

    def handle_event(self, event: str):
        """

        :param event:
        :return:
        """
        event = Web3.toJSON(event)
        print(f"in handle event {event}")

        publisher.push(event, topic=self.topic)

    async def log_loop(self, event_filter, poll_interval):
        """

        :param event_filter:
        :param poll_interval:
        :return:
        """
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            await asyncio.sleep(poll_interval)

    def run(self):
        # the event to listen to is static (unless SLA changes)
        event_filter = self.contract.events.AnswerUpdated.createFilter(fromBlock='latest')

        # block_filter = web3.eth.filter('latest')
        # tx_filter = web3.eth.filter('pending')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    self.log_loop(event_filter, 2)))
            # log_loop(block_filter, 2),
            # log_loop(tx_filter, 2)))
        finally:
            loop.close()
