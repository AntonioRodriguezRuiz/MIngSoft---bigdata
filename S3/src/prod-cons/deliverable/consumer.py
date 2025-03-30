from confluent_kafka import Consumer, KafkaError
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


# Configuración del consumidor
conf = {
    "bootstrap.servers": "localhost:9093",
    "group.id": "mi-grupo",
    "auto.offset.reset": "earliest",  # Lee desde el inicio si no hay offset guardado
}

consumer = Consumer(conf)

consumer.subscribe(["transactions"])


try:
    while True:
        # Polling de mensajes (timeout de 1 segundo)
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break
        # Mostrar el mensaje recibido
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    # Cerrar el consumidor de forma adecuada
    consumer.close()
