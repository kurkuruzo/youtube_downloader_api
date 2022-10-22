import pika
from api.settings import RABBITMQ_USER, RABBITMQ_PASS


def init_pika():
    params = pika.URLParameters(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@rabbit:5672")
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="youtube", durable=True)
    channel.exchange_declare("youtube", durable=True)
    channel.queue_bind("youtube", "youtube", routing_key="telegram")
    return channel


def send_download_confirmation(body):
    channel = init_pika()
    channel.basic_publish(exchange="youtube", routing_key="telegram", body=body)
