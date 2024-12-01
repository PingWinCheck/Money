import pika

from mail_service.connection import get_blocking_connection
from settings import settings
from typing import TYPE_CHECKING


def publisher(body: bytes):
    with get_blocking_connection() as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue=settings.rmq_queue, durable=True)
            channel.basic_publish(exchange='',
                                  routing_key=settings.rmq_queue,
                                  body=body,
                                  properties=pika.BasicProperties(delivery_mode=2))

