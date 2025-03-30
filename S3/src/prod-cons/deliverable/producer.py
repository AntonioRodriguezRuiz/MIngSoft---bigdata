from confluent_kafka import Producer
import csv
import json
from time import sleep
from typing import NamedTuple


class Register(NamedTuple):
    product_id: str
    product_name: str
    category: str
    discounted_price: str
    actual_price: str
    discount_percentage: str
    rating: str
    rating_count: str
    about_product: str
    user_id: str
    user_name: str
    review_id: str
    review_title: str
    review_content: str
    img_link: str
    product_link: str


conf = {"bootstrap.servers": "localhost:9093"}

producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        print(f"Error en la entrega: {err}")
    else:
        print(
            f"Mensaje entregado a {msg.topic()} [{msg.partition()}]: {msg.value().decode('utf-8')}"
        )


with open("amazon.csv", mode="r") as file:
    reader = csv.reader(file)
    registers = [Register(*row) for row in reader]

for register in registers:
    # Send the data as json
    producer.produce(
        "transactions",
        json.dumps(register._asdict()).encode("utf-8"),
        callback=delivery_report,
    )
    producer.poll(0)
    sleep(1)

producer.flush()
