from kafka import KafkaProducer
from kafka import KafkaConsumer

producer = KafkaProducer(bootstrap_servers=["115.238.44.226:39999"])
consumer = KafkaConsumer("pull_order_merchant", auto_offset_reset='earliest',
                         bootstrap_servers=["115.238.44.226:39999"])
