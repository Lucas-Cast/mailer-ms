from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.broker import BrokerClient
from app.core.db import get_async_session
from app.core.notification_strategy_factory import get_notification_strategy
from app.models.requests.notification_request import SendNotificationPayload


class NotificationService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
        broker: BrokerClient = Depends(BrokerClient),
    ):
        self._session = session
        self._broker = broker

    def publish_notification(
        self,
        payload: SendNotificationPayload,
    ) -> None:
        self._broker.publish(payload.model_dump_json(by_alias=True))

    async def send_notification(
        self,
        payload: SendNotificationPayload,
    ):
        notification_strategy = get_notification_strategy(payload)

        await notification_strategy.send_notification(payload)

        return {"message": "sent"}
