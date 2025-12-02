from collections.abc import Callable, Coroutine
from typing import Any

from aio_pika import Message, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractRobustConnection,
)

from app.core.constants import (
    BROKER_URL,
    DEAD_LETTER_EXCHANGE,
    DEAD_LETTER_QUEUE,
    NOTIFICATION_QUEUE,
)


class BrokerClient:
    def __init__(self):
        self._url: str = BROKER_URL
        self._queue_name: str = NOTIFICATION_QUEUE
        self._dead_letter_exchange: str = DEAD_LETTER_EXCHANGE
        self._dead_letter_queue: str = DEAD_LETTER_QUEUE
        self._connection: AbstractRobustConnection | None = None

    async def _get_connection(
        self,
    ) -> AbstractRobustConnection:
        if self._connection is None:
            self._connection = await connect_robust(self._url)
        return self._connection

    async def _declare_dead_letter_queue(self, channel: AbstractChannel) -> None:
        dlx = await channel.declare_exchange(
            name=self._dead_letter_exchange, type="direct", durable=True
        )
        dlq = await channel.declare_queue(name=self._dead_letter_queue, durable=True)
        await dlq.bind(dlx, routing_key=self._dead_letter_queue)

    async def _declare_main_queue(self, channel: AbstractChannel) -> AbstractQueue:
        return await channel.declare_queue(
            self._queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self._dead_letter_exchange,
                "x-dead-letter-routing-key": self._dead_letter_queue,
            },
        )

    async def publish(self, message: str | bytes, retry_count: int = 0) -> None:
        try:
            connection = await self._get_connection()

            async with connection:
                channel = await connection.channel()
                await self._declare_dead_letter_queue(channel)
                await self._declare_main_queue(channel)

                await channel.default_exchange.publish(
                    message=Message(
                        body=message.encode()
                        if not isinstance(message, bytes)
                        else message,
                        delivery_mode=2,
                        headers={"x-retry-count": retry_count},
                    ),
                    routing_key=self._queue_name,
                )

        except Exception as e:
            print(f" [!] Error publishing to queue: {e}")
            raise e

    async def consume(
        self,
        callback_function: Callable[..., Coroutine[Any, Any, None]],
        queue_name: str,
        max_retries: int,
    ) -> None:
        print(f" [*] Connecting to queue '{queue_name}'...")
        connection = await self._get_connection()

        async with connection:
            channel = await connection.channel()
            print(f" [*] Connected to queue '{queue_name}'.")

            await channel.set_qos(prefetch_count=1)
            await self._declare_dead_letter_queue(channel)
            await self._declare_main_queue(channel)

            consumed_queue = await channel.get_queue(queue_name)

            async with consumed_queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        await callback_function(
                            message,
                            message.headers.get("x-last-error", None),
                        )
                        await message.ack()
                        print(f" [V] Message processed successfully for {queue_name}.")
                    except Exception as e:
                        print(f" [!] Error processing message: {e}")
                        should_retry = await self._should_retry(
                            channel, max_retries, message, e
                        )
                        if should_retry:
                            await message.ack()
                        else:
                            await message.nack(requeue=False)

    async def _should_retry(
        self,
        channel: AbstractChannel,
        max_retries: int,
        message: AbstractIncomingMessage,
        e: Exception,
    ) -> bool:
        retry_count = message.headers.get("x-retry-count", None)
        if not isinstance(retry_count, int):
            return False

        if retry_count < max_retries:
            retry_count += 1
            print(f" [!] Retrying message ({retry_count}/{max_retries})...")

            await channel.default_exchange.publish(
                message=Message(
                    body=message.body,
                    delivery_mode=2,
                    headers={"x-retry-count": retry_count, "x-last-error": str(e)},
                ),
                routing_key=self._queue_name,
            )

            return True

        print(
            f" [X] Max retries reached ({max_retries}). Sending to dead letter queue."
        )
        return False
