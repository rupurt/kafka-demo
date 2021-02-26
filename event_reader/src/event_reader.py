from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable
import logging
import json
import os
import time
import psycopg2 as pg
from sqlalchemy import create_engine

# touch to add comments
LINK_QUERY = """
SELECT  ABS(ROUND((1. - (x.price*2./(y.price + z.price)))*100, 3)) || ' ' ||'%%' as deviation
FROM(

WITH tmp as
(
SELECT (event -> 'args' ->> 'current') ::numeric as contract_price,
event -> 'args' ->> 'roundId' as round_id,
event ->> 'transactionIndex' as trans_index,
event -> 'args' ->> 'updatedAt' as updated_at,
event ->> 'blockNumber' as block_number
FROM contract_price
WHERE event ->> 'event_type' = 'link-usd' AND event ->> 'blockNumber' =
(
select max(event ->> 'blockNumber') as max_block_number
FROM contract_price WHERE event ->> 'event_type' = 'link-usd'
)
)
SELECT contract_price/100000000. as price FROM tmp
WHERE tmp.trans_index =
(
select max(trans_index) as max_trans_index
FROM tmp
)
) x

JOIN
(SELECT (event -> 'chainlink' ->> 'usd')::numeric as price
FROM api_price WHERE event ->> 'event_type' = 'cg' order by updated_at desc limit 1
) y

ON 1=1

JOIN(
SELECT (event ->> 'close')::numeric as price  
FROM api_price WHERE event ->> 'event_type' = 'cp-link-usd' 
order by updated_at desc limit 1
) z

ON 1=1
"""


# touch to add comments
ETH_QUERY = """
SELECT  ABS(ROUND((1. - (x.price*2./(y.price + z.price)))*100, 3)) || ' ' ||'%%' as deviation
FROM(

WITH tmp as
(
SELECT (event -> 'args' ->> 'current') ::numeric as contract_price,
event -> 'args' ->> 'roundId' as round_id,
event ->> 'transactionIndex' as trans_index,
event -> 'args' ->> 'updatedAt' as updated_at,
event ->> 'blockNumber' as block_number
FROM contract_price
WHERE event ->> 'event_type' = 'eth-usd' AND event ->> 'blockNumber' =
(
select max(event ->> 'blockNumber') as max_block_number
FROM contract_price WHERE event ->> 'event_type' = 'eth-usd'
)
)
SELECT contract_price/100000000. as price FROM tmp
WHERE tmp.trans_index =
(
select max(trans_index) as max_trans_index
FROM tmp
)
) x

JOIN
(SELECT (event -> 'ethereum' ->> 'usd')::numeric as price
FROM api_price WHERE event ->> 'event_type' = 'cg' order by updated_at desc limit 1
) y

ON 1=1

JOIN(
SELECT (event ->> 'close')::numeric as price  
FROM api_price WHERE event ->> 'event_type' = 'cp-eth-usd' 
order by updated_at desc limit 1
) z

ON 1=1
"""

# touch to add comments
BTC_QUERY = """
SELECT  ABS(ROUND((1. - (x.price*2./(y.price + z.price)))*100, 3)) || ' ' ||'%%' as deviation
FROM(

WITH tmp as
(
SELECT (event -> 'args' ->> 'current') ::numeric as contract_price,
event -> 'args' ->> 'roundId' as round_id,
event ->> 'transactionIndex' as trans_index,
event -> 'args' ->> 'updatedAt' as updated_at,
event ->> 'blockNumber' as block_number
FROM contract_price
WHERE event ->> 'event_type' = 'btc-usd' AND event ->> 'blockNumber' =
(
select max(event ->> 'blockNumber') as max_block_number
FROM contract_price WHERE event ->> 'event_type' = 'btc-usd'
)
)
SELECT contract_price/100000000. as price FROM tmp
WHERE tmp.trans_index =
(
select max(trans_index) as max_trans_index
FROM tmp
)
) x

JOIN
(SELECT (event -> 'bitcoin' ->> 'usd')::numeric as price
FROM api_price WHERE event ->> 'event_type' = 'cg' order by updated_at desc limit 1
) y

ON 1=1

JOIN(
SELECT (event ->> 'close')::numeric as price  
FROM api_price WHERE event ->> 'event_type' = 'cp-btc-usd' 
order by updated_at desc limit 1
) z

ON 1=1
"""



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
                # touch to add comments
                self.logger.debug(f"LINK: {list(self.db.execute(LINK_QUERY))[0]}")
                self.logger.debug(f"ETH: {list(self.db.execute(ETH_QUERY))[0]}")
                self.logger.debug(f"BTC: {list(self.db.execute(BTC_QUERY))[0]}")

                # self.logger.debug(message.value)

