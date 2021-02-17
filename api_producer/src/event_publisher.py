from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import os
import time
import logging


class Publisher:
    """
    Abstracts a kafka producer
    """
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

    # this is a good standalone method
    def push(self, message: str, topic: str):
        """

        :param message:
        :param topic:
        :return:
        """
        self.logger.info(f"Publishing: {message}")
        try:
            if self.producer:
                self.producer.send(topic,
                                   bytes(json.dumps(message).encode('utf-8')))
        except AttributeError:
            self.logger.error(f"Unable to send {message}. The producer does not exist.")


