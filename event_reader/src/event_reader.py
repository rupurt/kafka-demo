from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable
import logging
import json
import os
import time
import psycopg2 as pg
from sqlalchemy import create_engine

# TODO:  create tables in the Reader constructor instead of the init.sql script
db_name = os.getenv('DB_NAME', 'ENV VARIABLE DB_NAME NOT FOUND!')
db_user = os.getenv('DB_USER', 'ENV VARIABLE DB_USER NOT FOUND!')
db_pass = os.getenv('DB_PASSWORD', 'ENV VARIABLE DB_PASSWORD NOT FOUND!')
db_host = 'store'
db_port = '5432'

# Connect to the database
db_string = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'


class ConnectionException(Exception):
    pass


class Reader:

    def __init__(self, topic: str, target_table: str, value_deserializer=lambda x: json.loads(x.decode('utf-8'))):
        """
        Kafka consumer abstraction
        :param topic:
        :param target_table: table to be created and populated in the DB
        :param value_deserializer:
        """

        self.db = create_engine(db_string)
        self.logger = logging.getLogger()
        self.logger.debug("Initializing the consumer")
        self.topic = topic
        self.value_deserializer = value_deserializer
        self.target_table = target_table

        while not hasattr(self, 'consumer'):
            self.logger.debug("Getting the kafka consumer")
            try:
                self.consumer = KafkaConsumer(bootstrap_servers="kafka:9092",
                                              consumer_timeout_ms=10,
                                              auto_offset_reset='earliest',
                                              group_id='test_consumer_group',
                                              value_deserializer=self.value_deserializer
                                              )
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

    def run(self):
        """
        Process messages from broker
        :return:
        """
        # self.logger.debug(f"Reading stream: {self.topic}")
        if self.consumer:
            for message in self.consumer:
                self.db.execute(f"INSERT INTO {self.target_table}(event) VALUES ('{message.value}');")
                self.logger.debug(f"TABLE COUNT: {list(self.db.execute(f'SELECT COUNT(*) FROM {self.target_table};'))}")
                self.logger.debug(message.value)

