from api_reader import APIHook
import time
import logging
import json
import os

api_publisher = APIHook(topic='apis')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


if __name__ == '__main__':

    logging.info("Dispatching API")
    api_publisher.run()
