from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

for msg in consumer:
    print("Received:", msg.value)
    # INSERT INTO PostgreSQL here