import json
from collections.abc import Callable
from typing import Any

from pika import BasicProperties, BlockingConnection, URLParameters

from app.core.constants import BROKER_URL, QUEUE_NAME


class BrokerClient:
    def __init__(self):
        self._url: str = BROKER_URL
        self._queue_name: str = QUEUE_NAME

    def _get_connection(self) -> BlockingConnection:
        params = URLParameters(self._url)
        return BlockingConnection(params)

    def publish(self, message: dict[str, Any] | str) -> None:
        connection = None
        try:
            connection = self._get_connection()
            channel = connection.channel()

            channel.queue_declare(queue=self._queue_name, durable=True)

            if isinstance(message, dict):
                body = json.dumps(message)
            else:
                body = message

            channel.basic_publish(
                exchange="",
                routing_key=self._queue_name,
                body=body,
                properties=BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                ),
            )

        except Exception as e:
            print(f" [!] Error publishing to queue: {e}")
            raise e
        finally:
            if connection and connection.is_open:
                connection.close()

    def consume(self, callback_function: Callable[..., None]) -> None:
        print(f" [*] Connecting to queue '{self._queue_name}'...")
        connection = self._get_connection()
        channel = connection.channel()

        channel.queue_declare(queue=self._queue_name, durable=True)

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=self._queue_name, on_message_callback=callback_function
        )

        print(" [*] Waiting for messages.")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print(" [!] Stopping consumer...")
            channel.stop_consuming()
            connection.close()
