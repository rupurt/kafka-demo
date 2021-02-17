from api_reader import APIHook
import time
import logging
import json
import os

api_publisher = APIHook(topic='apis')
# contract_publisher = ContractHook(address=address, abi=abi, topic='contracts')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


if __name__ == '__main__':
    # port = int(os.environ["DB_PORT"])  # 5432

    logging.info("Dispatching API")
    api_publisher.run()
