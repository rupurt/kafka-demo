## Kafka Demo ##
 
This repo was written as part of a job interview and isn't necessarily a good
example of a production Kafka use case.  

* `docker-compose.yml`
  * This is the base composition.  It should allow you to bring up the stack 
  with just `docker-compose up`
* `docker-compose.dev.yml`
  * To be written
* producer
  * The source and `Dockerfile` for the producer application.
* consumer
  * Same thing but for the consumer
* tester  
  * Integration tests -  to be done
  
### Dependencies ###
Mention docker version etc..

### Example Usage ###


#### Manual Testing ####
Run
```bash
docker-compose up
```

In another terminal you can then run:
```bash
docker exec -it kafka-demo_store_1 psql -U postgres -a kafka_sink -c "SELECT * FROM contract_price;"
```

```bash
docker exec -it kafka-demo_store_1 psql -U postgres -a kafka_sink -c "SELECT * FROM contract_price;"
```

#### Scripted Testing ####



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

