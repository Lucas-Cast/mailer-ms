import asyncio
import json
from typing import Any

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from pydantic import TypeAdapter

from app.core.broker import BrokerClient
from app.core.db import async_session_factory
from app.models.requests.notification_request import SendNotificationPayload
from app.services.notification_service import NotificationService

notification_type_adapter: TypeAdapter[SendNotificationPayload] = TypeAdapter(
    SendNotificationPayload
)


async def process_notification_task(raw_payload: dict[str, Any]) -> None:
    async with async_session_factory() as session:
        broker = BrokerClient()

        payload: SendNotificationPayload = notification_type_adapter.validate_python(
            raw_payload
        )

        service = NotificationService(session=session, broker=broker)

        await service.send_notification(payload)


def on_message(
    ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
) -> None:
    try:
        message_data = json.loads(body)

        asyncio.run(process_notification_task(message_data))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f" [x] Processed message delivery tag: {method.delivery_tag}")

    except Exception as e:
        print(f"Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


if __name__ == "__main__":
    broker = BrokerClient()
    broker.consume(on_message)
