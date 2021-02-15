from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable
import logging
import json
import os
import time
import psycopg2 as pg
from sqlalchemy import create_engine

# inject from environment variables
db_name = 'kafka_sink'
db_user = 'postgres'
db_pass = 'secret'
db_host = 'store'
db_port = '5432'

# Connect to the database
db_string = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'


class ConnectionException(Exception):
    pass


class Reader:

    def __init__(self, topic):
        # conn_string = "dbname='kafka_sink' user='postgres'"
        # self.conn = pg.connect(conn_string)
        # self.cur = self.conn.cursor()
        self.db = create_engine(db_string)
        self.logger = logging.getLogger()
        self.logger.debug("Initializing the consumer")
        self.topic = topic
        while not hasattr(self, 'consumer'):
            self.logger.debug("Getting the kafka consumer")
            try:
                self.consumer = KafkaConsumer(bootstrap_servers="kafka:9092",
                                              consumer_timeout_ms=10,
                                              auto_offset_reset='earliest',
                                              group_id='test_consumer_group',
                                              value_deserializer=lambda x: x.decode('utf-8'))
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
                self.db.execute(f"INSERT INTO coingecko(event) VALUES ('{message.value}');")
                self.logger.debug(f"TABLE COUNT: {list(self.db.execute('SELECT COUNT(*) FROM coingecko;'))}")
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