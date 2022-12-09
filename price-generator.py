#!/usr/bin/python3

import asyncio
import time
import random
import json
import os
from aiokafka import AIOKafkaProducer

producers_pool = 8

def serializer(value):
    return json.dumps(value).encode()

async def produce_prices():

    ## Create producers pool

    producer = [0] * producers_pool

    print(f"Starting price producers pool of {producers_pool} instance(s)...")
    for i in range(producers_pool):
        while True:
            try:
                producer[i] = AIOKafkaProducer(
                            bootstrap_servers=os.getenv('KAFKA_HOST', 'localhost:9092'),
                            value_serializer=serializer,
                            enable_idempotence=True )
                await producer[i].start()
                break
            except:
                await producer[i].stop()
                time.sleep(1)

    ## Declare runtime variables

    loop_duration = 1000000 #ns
    loop_nexttime = time.perf_counter_ns()
    producer_current = 0
    sent_total = 0
    sent_current = 0
    starttime = int(time.time())
    reported = 0

    ## Workload

    while True:

        if producer_current > (producers_pool - 1):
            producer_current = 0

        while time.perf_counter_ns() < loop_nexttime:
            try:
                time.sleep(0.0001)
            except KeyboardInterrupt:
                print(" Signal received in sleep. Stoping producers pool...")
                for i in range(producers_pool):
                    await producer[i].stop()
                print("Done.")
                return

        loop_nexttime += loop_duration

        if (time.time() - reported) >= 1 & sent_total > 0:
            reported = time.time()
            runtime = time.time() - starttime
            print(f'Produced {sent_total} prices in { int(runtime) }s with avg[{ round(sent_total / runtime, 1) }], cur[{ round(sent_current / 1, 1) }] prices/s')
            sent_current = 0

        try:

            prices = {}
            bids = {}
            asks = {}
            stats = {}
            bids_sum = 0
            asks_sum = 0

            for i in range(50):

                if i == 0:
                    bid = round(random.uniform(1.00, 10.00), 2)
                    ask = round(random.uniform(1.00, 10.00), 2)
                elif i == 49:
                    bid = round(random.uniform(1.00, 500.00), 2)
                    ask = round(random.uniform(1.00, 500.00), 2)
                else:
                    bid = round(random.uniform(1.00, 20.00), 2)
                    ask = round(random.uniform(1.00, 20.00), 2)

                bids.update({'bid_' + str(i + 1).zfill(2): bid})
                asks.update({'ask_' + str(i + 1).zfill(2): ask})

                bids_sum += bid
                asks_sum += ask

            stats = { 'avg_bid': round(bids_sum / 50, 4), 'avg_ask': round(asks_sum / 50, 4) }
            prices = { 'timestamp': int(time.time()), **bids, **asks, 'stats': str(stats) }

            # Round-robin
            await producer[producer_current].send("prices", prices)
            producer_current += 1

            sent_total += 1
            sent_current += 1

        except KeyboardInterrupt:
            print(" Signal received in loop. Stoping producers pool...")
            for i in range(producers_pool):
                await producer[i].stop()
            print("Done.")
            return

    else:
        print("Stoping producers pool...")
        for i in range(producers_pool):
            await producer[i].stop()
        print("Done.")

asyncio.run(produce_prices())
