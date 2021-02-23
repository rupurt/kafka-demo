from contract_reader import ContractHook
import time
import logging
import json
import asyncio

# TODO: remember to account for more chains, not just more price pair feeds

contract_publisher = ContractHook(topic='contracts')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


if __name__ == '__main__':
    logging.debug("Dispatching Contract")
    asyncio.run(contract_publisher.run())
