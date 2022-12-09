#!/usr/bin/python3

import asyncio
import json
import time
import requests
import os
from aiokafka import AIOKafkaConsumer

def deserializer(serialized):
    return json.loads(serialized)

def notify_telegram(text):
    token = "5943041240:AAFSeeEaDQ2G5lCGzhUPgc1MZAmeJiE9GLE"
    chat_id = "-1001502872941"
    url_req = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
        token,
        chat_id,
        requests.utils.quote(text) )
    requests.get(url_req)

async def consume_prices():

    print(f"Starting prices monitor consumer...")
    while True:
        try:
            consumer = AIOKafkaConsumer(
                'prices',
                bootstrap_servers=os.getenv('KAFKA_HOST', 'localhost:9092'),
                value_deserializer=deserializer,
                auto_offset_reset='latest' )
            await consumer.start()
            break
        except:
            await consumer.stop()
            time.sleep(1)

    try:

        async for msg in consumer:
            target = (msg.value['ask_01'] + msg.value['bid_01']) / 2
            if target > 9.9:
                notification = 'ask_01 [{}] + bid_01 [{}] / 2 = {}'.format(
                    str(msg.value['ask_01']),
                    str(msg.value['bid_01']),
                    str(round(target, 2)) )
                print(f"Notification: {notification}")
                notify_telegram(notification)

    except KeyboardInterrupt:
        print(" Signal received.")

    finally:
        print("Stoping consumer...")
        await consumer.stop()
        print("Done.")

asyncio.run(consume_prices())
