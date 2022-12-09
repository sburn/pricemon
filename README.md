pricemon demo
=============

This solution uses the latest `Zookeeper` and `Kafka` docker images from Confluent, official `Clickhouse` and
two custom services written on `Python3`: `price-generator` and `price-monitor`. The first one generates
1 row of test data milisecond and writes it to Kafka. The second consumes hot test data from Kafka
and sends notification with minimal latency to Telegram channel as monitored trigger arrives. Clickhouse
server includes a Kafka integration which writes test data from a queue to a table for a future use in a
cold state.

Actual versions of `docker`, `docker-compose` and `git` are reqiured to run this demo.

Basic Usage
-----------

1. Pull the project:

```bash
git pull https://github.com/sburn/pricemon.git
cd pricemon
```

2. Start project services as docker containers:

```bash
docker-compose up -d
```

3. Join private Telegram channel to receive demo notifications by link:

```bash
https://t.me/+Zaf7m1ozc_plOTJi
```

To stop project services:

```bash
docker-compose down
```

Additional usage
----------------

To check `price-generator` performance, look at container logs:

```bash
docker logs --follow pricemon_generator_1
```

To run `price-generator` interactively, make sure you have `python3`, then install Python requirements
and run the service with `KAFKA_HOST` environment variable set to docker container address:

```bash
pip3 install asyncio aiokafka
KAFKA_HOST=172.16.100.11:9092 ./price-generator.py
```

`price-generator` output example:

```bash
Starting price producers pool of 8 instance(s)...
Produced 1 prices in 0s with avg[1.0], cur[1.0] prices/s
Produced 1003 prices in 1s with avg[512.2], cur[1002.0] prices/s
Produced 2005 prices in 2s with avg[677.4], cur[1002.0] prices/s
Produced 3007 prices in 3s with avg[759.0], cur[1002.0] prices/s
Produced 4009 prices in 4s with avg[807.6], cur[1002.0] prices/s
Produced 5011 prices in 5s with avg[839.9], cur[1002.0] prices/s
Produced 6011 prices in 6s with avg[862.8], cur[1000.0] prices/s
Produced 7013 prices in 7s with avg[880.1], cur[1002.0] prices/s
Produced 8013 prices in 8s with avg[893.4], cur[1000.0] prices/s
Produced 9015 prices in 9s with avg[904.2], cur[1002.0] prices/s
Produced 10001 prices in 10s with avg[911.6], cur[986.0] prices/s
```
