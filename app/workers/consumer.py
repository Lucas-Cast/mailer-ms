import asyncio
import json
from collections.abc import Callable, Coroutine
from typing import Any

from aio_pika.message import IncomingMessage
from pydantic import TypeAdapter

from app.core.broker import BrokerClient
from app.core.constants import (
    DEAD_LETTER_QUEUE,
    DEAD_LETTER_QUEUE_MAX_RETRIES,
    NOTIFICATION_QUEUE,
    NOTIFICATION_QUEUE_MAX_RETRIES,
)
from app.core.db import async_session_factory
from app.models.enums.notification_status_enum import NotificationStatusEnum
from app.models.requests.notification_request import (
    MessageBrokerPayload,
)
from app.services.notification_service import NotificationService

notification_type_adapter: TypeAdapter[MessageBrokerPayload] = TypeAdapter(
    MessageBrokerPayload
)

TaskType = Callable[[IncomingMessage, Exception | None], Coroutine[Any, Any, None]]


async def process_notification_task(
    message: IncomingMessage, queue_name: str, error: Exception | None = None
) -> None:
    raw_payload = json.loads(message.body.decode())

    async with async_session_factory() as session:
        broker = BrokerClient()

        payload: MessageBrokerPayload = notification_type_adapter.validate_python(
            raw_payload
        )

        service = NotificationService(session=session, broker=broker)

        if queue_name == NOTIFICATION_QUEUE:
            await service.send_notification(
                log_id=payload.log_id, payload=payload.payload
            )
        elif queue_name == DEAD_LETTER_QUEUE:
            await service.update_log_status(
                log_id=payload.log_id,
                notification_status=NotificationStatusEnum.FAILED,
                error_message=error.__str__() if error else "Unknown error",
            )


async def main() -> None:
    broker = BrokerClient()
    notification_task: TaskType = lambda msg, _: process_notification_task(
        msg, NOTIFICATION_QUEUE
    )
    dead_letter_task: TaskType = lambda msg, err: process_notification_task(
        msg, DEAD_LETTER_QUEUE, err
    )

    await asyncio.gather(
        broker.consume(
            notification_task,
            NOTIFICATION_QUEUE,
            max_retries=NOTIFICATION_QUEUE_MAX_RETRIES,
        ),
        broker.consume(
            dead_letter_task,
            DEAD_LETTER_QUEUE,
            max_retries=DEAD_LETTER_QUEUE_MAX_RETRIES,
        ),
        return_exceptions=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
