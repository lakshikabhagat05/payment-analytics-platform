from kafka 
import KafkaProducer
import json
import random
import time 

producer = kafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = lambda v:json.dumps(v).encode("utf-8")
)
while True:
    transaction = {
        "user_id": random.randint(1,100),
        "amount": random.randint(10,50000),
        "status": "SUCCESS"
    }
    producer.send("transactions",transaction)
    print("Sent:",transaction)
    time.sleep(2)
    