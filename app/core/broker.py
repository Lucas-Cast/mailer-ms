from collections.abc import Callable, Coroutine
from typing import Any

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractRobustConnection

from app.core.constants import BROKER_URL, QUEUE_NAME


class BrokerClient:
    def __init__(self):
        self._url: str = BROKER_URL
        self._queue_name: str = QUEUE_NAME

    async def _get_connection(
        self,
    ) -> AbstractRobustConnection:
        return await connect_robust(self._url)

    async def publish(self, message: str) -> None:
        connection = None
        try:
            connection = await self._get_connection()

            async with connection:
                routing_key = self._queue_name

                channel = await connection.channel()

                await channel.declare_queue(self._queue_name, durable=True)

                await channel.default_exchange.publish(
                    message=Message(body=message.encode()),
                    routing_key=routing_key,
                )

        except Exception as e:
            print(f" [!] Error publishing to queue: {e}")
            raise e

    async def consume(
        self, callback_function: Callable[..., Coroutine[Any, Any, None]]
    ) -> None:
        print(f" [*] Connecting to queue '{self._queue_name}'...")
        connection = await self._get_connection()

        async with connection:
            print(" [*] Connected.")
            channel = await connection.channel()

            await channel.set_qos(prefetch_count=1)

            queue = await channel.declare_queue(self._queue_name, durable=True)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        await callback_function(message)

        print(" [*] Waiting for messages.")
