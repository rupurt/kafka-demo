from api_reader import APIHook
import time
import logging
import json
import os

coinpaprika_url = "https://api.coinpaprika.com/v1/coins/"
coin_ids = ["btc-bitcoin/ohlcv/today", "eth-ethereum/ohlcv/today", "link-chainlink/ohlcv/today"]


base = "ethereum,bitcoin,chainlink"
vs = "usd"
coingecko_url = "https://api.coingecko.com/api/v3/simple/price"

cg_params = {
            'ids': base,
            'vs_currencies': vs
         }

api_hook = APIHook(topic='apis')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


if __name__ == '__main__':

    while True:
        logger.info("Calling API")
        api_hook.fetch(base_url=coingecko_url, params=cg_params, event_type='cg')
        for coin_id in coin_ids:
            time.sleep(1)
            event_type = coin_id.split("-")[0]
            api_hook.fetch_custom(base_url=coinpaprika_url, params=coin_id, event_type=f"cp-{event_type}-usd")
        time.sleep(15)
