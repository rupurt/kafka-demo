from kafka import KafkaConsumer, TopicPartition
from event_reader import Reader, ConnectionException
import logging
import json

# app = Flask(__name__)
reader = Reader()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


# @app.route("/")
# def index():
#     return "This is the Event reader.  To read an event from the stream " + \
#            "issue a GET on the /events endpoint."
#
#
# @app.route("/events", methods=['GET'])
# def read_event():
#     try:
#         message = reader.next()
#     except ConnectionException:
#         return json.dumps({
#             'status': 'connection_error',
#             'message': 'Unable to read from the message stream.'}), 500
#
#     app.logger.debug("Read this data from the stream: {0}".format(message))
#     if message:
#         return json.dumps(message), 200
#     return "", 204


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
        reader.next()
    # app.run(host='0.0.0.0', port=80, debug=True)
