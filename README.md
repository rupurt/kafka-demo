## Kafka Demo ##
 
Near real-time data pipeline that evaluates the accuracy of price feed contracts with respect to two free cryptocurrency APIs,
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
  * Basic Kafka setup: 1 broker, 2 topics with one partition each and replication factor of 1 (due to there being only one broker). This setup is not suitable for a production environment.
* zookeeper
  * Kafka configuration manager. Single instance.
* api_producer
  * The source and `Dockerfile` for the producer application.
* producer
  * The source and `Dockerfile` for the producer application.
* api_consumer
  * Same thing but for the consumer
* consumer
  * Same thing but for the consumer
* store
  * Persistent layer: TimescaleDB (Postgresql extension). Time-series DB designed to support high insert rates and fast time-based queries. 

* admin
  * Adminer: Light-weight UI-based database management tool that can be used to quickly visualize the tables and run analytics queries.
  
* tester  
  * Integration tests -  to be done
  
### Requirements ###
Docker-compose. Version used for this project: 1.24.0. Should work with other versions as well.

### Example Usage ###


#### Testing ####
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



### Dev Mode ###


*Make sure you run `docker-compose down` before switching to dev mode.*

### Known Issues and Other things to worry about ###

This is just a quick demo of kafka's pub sub using Python.  It's missing _a lot_ of 
stuff you would want if you were going to use this in a production environment.  Including:
* payload validation
* authentication and authorization
* improved error handling
* connection retries for kafka brokers
* managing partitions
* probably other things

