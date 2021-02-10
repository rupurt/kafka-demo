from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable
import logging
import json
import os
import time


# topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'


class ConnectionException(Exception):
    pass


class Reader:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.debug("Initializing the consumer")
        self.topic = 'stats'
        while not hasattr(self, 'consumer'):
            self.logger.debug("Getting the kafka consumer")
            try:
                self.consumer = KafkaConsumer(bootstrap_servers="kafka:9092",
                                              consumer_timeout_ms=10,
                                              auto_offset_reset='earliest',
                                              group_id='test_consumer_group',
                                              value_deserializer=lambda x: json.loads(x.decode('utf-8')))
            except NoBrokersAvailable as err:
                self.logger.error(f"Unable to find a broker: {err}")
                time.sleep(1)

        self.logger.debug(f"We have a consumer {time.time()}")
        self.consumer.subscribe(self.topic)
        # Wait for the topic creation and seek back to the beginning
        self.consumer.poll(timeout_ms=10000)
        # Kafka can figure out if the offset is valid or not.
        # For an invalid offset, it is automatically advanced to the next valid offset.
        # If you seek to offset zero, you will always get the oldest message that is stored.
        self.consumer.seek(TopicPartition(self.topic, 0), 0)
        self.logger.debug(f"ok {time.time()}")

    def next(self):
        """
        Get the "next" event.  This is a pretty naive implementation.  It
        doesn't try to deal with multiple partitions or anything and it assumes
        the event payload is json.
        :return: The event in json form
        """
        # self.logger.debug(f"Reading stream: {self.topic}")

        if self.consumer:
            for message in self.consumer:
                #if message is None or not message.value:
                #    continue
                self.logger.debug(message.value)

    # try:
    #     if self.consumer:
    #         self.logger.debug("A consumer is calling 'next'")
    #         try:
    #             # This would be cleaner using `next(consumer)` except
    #             # that there is no timeout on that call.
    #             event_partitions = self.consumer.poll(timeout_ms=100,
    #                                                   max_records=1)
    #             event_list = list(event_partitions.values())
    #             payload = event_list[0][0]
    #             event = payload.value
    #             self.logger.info(f'Read an event from the stream {event} of type({event})')
    #             try:
    #                 return json.loads(event)
    #             except json.decoder.JSONDecodeError:
    #                 return json.loads(f'{{ "message": "{event}" }}')
    #         except (StopIteration, IndexError):
    #             return None
    #     raise ConnectionException
    # except AttributeError as ae:
    #     self.logger.error("Unable to retrieve the next message.  "
    #                       "There is no consumer to read from.")
    #     self.logger.error(str(ae))
    #     raise ConnectionException