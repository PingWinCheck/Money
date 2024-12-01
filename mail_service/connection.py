import pika
from settings import settings


def get_blocking_connection():
    return pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=settings.rmq_host,
            port=settings.rmq_port,
            credentials=pika.PlainCredentials(username=settings.rmq_user,
                                              password=settings.rmq_pass))
    )