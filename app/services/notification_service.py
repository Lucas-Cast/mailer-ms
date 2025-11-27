from fastapi import Depends
from sqlalchemy import update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.broker import BrokerClient
from app.core.db import get_async_session
from app.core.notification_strategy_factory import get_notification_strategy
from app.models.entities.notification_log import NotificationLog
from app.models.enums.notification_status_enum import NotificationStatusEnum
from app.models.requests.notification_request import (
    MessageBrokerPayload,
    SendNotificationPayload,
)


class NotificationService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
        broker: BrokerClient = Depends(BrokerClient),
    ):
        self._session = session
        self._broker = broker

    async def publish_notification(
        self,
        payload: SendNotificationPayload,
    ) -> str:
        log_id = await self.log_notification(payload)

        json_payload = MessageBrokerPayload(
            log_id=log_id, payload=payload
        ).model_dump_json(by_alias=True)

        try:
            await self._broker.publish(json_payload)
            return f"Published notification: {json_payload}"

        except Exception as e:
            await self.update_log_status(
                log_id=log_id,
                notification_status=NotificationStatusEnum.FAILED,
                error_message=str(e),
            )
            raise

    async def send_notification(
        self,
        log_id: str,
        payload: SendNotificationPayload,
    ) -> None:
        notification_strategy = get_notification_strategy(payload)

        try:
            await notification_strategy.send_notification(payload)
            await self.update_log_status(
                log_id=log_id, notification_status=NotificationStatusEnum.SENT
            )
        except Exception as e:
            await self.update_log_status(
                log_id=log_id,
                notification_status=NotificationStatusEnum.FAILED,
                error_message=str(e),
            )
            raise

    async def log_notification(
        self,
        payload: SendNotificationPayload,
        notification_status: NotificationStatusEnum = NotificationStatusEnum.PENDING,
        error_message: str | None = None,
    ) -> str:
        notification_log = NotificationLog(
            body=payload.body,
            recipient=payload.recipient.email,
            notification_type_id=payload.type,
            notification_status_id=notification_status,
            error_message=error_message,
        )

        self._session.add(notification_log)
        await self._session.commit()
        return notification_log.id

    async def update_log_status(
        self,
        log_id: str,
        notification_status: NotificationStatusEnum,
        error_message: str | None = None,
    ) -> None:
        statement = (
            update(NotificationLog)
            .where(NotificationLog.id == log_id)  # type: ignore
            .values(
                notification_status_id=notification_status,
                error_message=error_message,
            )
        )
        await self._session.exec(statement)
        await self._session.commit()
