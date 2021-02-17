from kafka import KafkaConsumer, TopicPartition
from event_reader import Reader, ConnectionException
import logging
import json
import time
import socket

# app = Flask(__name__)
api_reader = Reader(topic='apis', target_table='api_price', value_deserializer=lambda x: x.decode('utf-8'))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


if __name__ == '__main__':
    # wait for DB to be reachable
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect(('store', 5432))
            s.close()
            break
        except socket.error as ex:
            time.sleep(0.1)
    while True:
        api_reader.run()
