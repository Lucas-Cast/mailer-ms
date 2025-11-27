import asyncio
import json

from aio_pika.message import IncomingMessage
from pydantic import TypeAdapter

from app.core.broker import BrokerClient
from app.core.db import async_session_factory
from app.models.requests.notification_request import (
    MessageBrokerPayload,
)
from app.services.notification_service import NotificationService

notification_type_adapter: TypeAdapter[MessageBrokerPayload] = TypeAdapter(
    MessageBrokerPayload
)


async def process_notification_task(message: IncomingMessage) -> None:
    raw_payload = json.loads(message.body.decode())

    async with async_session_factory() as session:
        broker = BrokerClient()

        payload: MessageBrokerPayload = notification_type_adapter.validate_python(
            raw_payload
        )

        service = NotificationService(session=session, broker=broker)

        await service.send_notification(log_id=payload.log_id, payload=payload.payload)
        print("[V] Notification successfully sent")


if __name__ == "__main__":
    broker = BrokerClient()
    asyncio.run(broker.consume(process_notification_task))
