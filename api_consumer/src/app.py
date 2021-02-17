from kafka import KafkaConsumer, TopicPartition
from event_reader import Reader, ConnectionException
import logging
import json

# app = Flask(__name__)
api_reader = Reader(topic='apis', target_table='api_price', value_deserializer=lambda x: x.decode('utf-8'))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


if __name__ == '__main__':
    # topic = 'stats'
    # logging.info("Reading")
    # consumer = KafkaConsumer(
    #                          bootstrap_servers="kafka:9092",
    #                          consumer_timeout_ms=1000,
    #                          auto_offset_reset='earliest',
    #                          group_id='test_consumer_group',
    #                          value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    #
    # consumer.subscribe(topic)
    # consumer.poll(timeout_ms=30000)
    # consumer.seek(TopicPartition(topic, 0), 0)

    # for message in consumer:
    #     print(message)
    while True:
        # contract_reader.run()
        api_reader.run()
    # app.run(host='0.0.0.0', port=80, debug=True)