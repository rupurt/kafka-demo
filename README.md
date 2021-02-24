## Kafka Demo ##
 
Near real-time data pipeline that evaluates the accuracy of price feed contracts with respect to two public cryptocurrency APIs,
Coingecko and Coinpaprika, for 3 pairs: ETH-USD, LINK-USD and BTC-USD. The metric used for the accuracy is the percentage difference between the 
values returned by the contracts and the average value returned by the APIs.

N.B.: This repo was written as part of a job interview and isn't necessarily a good
example of a production Kafka use case.  

* `docker-compose.yml`
  * This is the base composition.  It allows you to bring up the stack 
  with just `docker-compose up`. Please be patient as downloading images will take a while. 
    Don't forget to run `docker-compose down` when finished! 

#### Services ####

* kafka
  * Basic Kafka setup: 1 broker, 2 topics (`contracts` and `apis`) with one partition each and replication factor of 1 (due to there being only one broker). This setup is not suitable for a production environment.
* zookeeper
  * Kafka configuration manager. Single instance.
* api_producer
  * The source and `Dockerfile` for the API Producer service. Instantiates a Kafka Producer and sends synchronous requests to the relevant APIs
  by polling, then publishes the messages to the `apis` topic.
* producer
  * The source and `Dockerfile` for the Contract Producer service. Instantiates a Kafka Producer and listens asynchronously 
    for events of type `AnswerUpdated` on the relevant price feeds, then publishes the messages to the `contracts` topic.
* api_consumer
  * The source and `Dockerfile` for the API Consumer service. Consumes messages from the `api` topic and inserts into
  the `api_price` table.
* consumer
  * The source and `Dockerfile` for the Contract Consumer service. Consumes messages from the `contracts` topic and inserts into
  the `contract_price` table.
* store
  * TimescaleDB (Postgresql extension). Time-series DB designed to support high insert rates and fast time-based queries. 

* admin
  * Adminer: Light-weight UI-based database management tool that can be used to quickly visualize the tables and run analytics queries against TimescaleDB.
  
* tester  
  * Integration tests -  to be done
  
### Requirements ###
Docker-compose. Version used for this project: 1.24.0. Not guaranteed to work with other versions.
### Set up ###
Create an Infura project and copypaste the project id into an env file on the root level called `producer.env`, like this:
`INFURA_PROJECT_ID = <YOUR-PROJECT-ID>`

Similarly create `database.env` `api_consumer.env` `consumer.env` with the following ENV variables:
`DB_USER=postgres`
`DB_PASSWORD=<YOUR-PASSWORD>`
`DB_NAME=kafka_sink`

### Add new APIs and contract feeds ###
If you wish to add a new price feed contract simply specify the desired address and abi in the `config.ini` file.

If you wish to add a new API please leverage the `fetch` (for standard GET and POST requests) and `fetch_custom` (for custom requests, e.g. get with path parameters)
from the `APIHook` class. Additionally you might need to write a dedicated transform method in case the response is not in a JSON format.

#### Demo Run ####
Run
```bash
docker-compose up
```

In another terminal you can then run:
```bash
docker exec -it kafka-demo_store_1 psql -U postgres -a kafka_sink -c "SELECT * FROM contract_price;"
```

```bash
docker exec -it kafka-demo_store_1 psql -U postgres -a kafka_sink -c "SELECT * FROM api_price;"
```


### Querying basics ###

Both target tables store event data in a jsonb column called `event`. You can query by making use of Postgres JSON operators. 
For example use the following query to get the latest ETH price from the coingecko 'cg' API:

`SELECT (event -> 'ethereum' ->> 'usd')::numeric as price  
FROM api_price WHERE event ->> 'event_type' = 'cg' order by updated_at desc limit 1`

### Known Issues and Other things to worry about ###

This is just a quick demo of kafka's pub sub using Python.  It's missing _a lot_ of 
stuff you would want if you were going to use this in a production environment.  Including:
* payload validation
* authentication and authorization
* improved error handling
* managing partitions
* probably other things

