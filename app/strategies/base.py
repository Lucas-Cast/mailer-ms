from typing import Generic, Protocol

from app.models.requests.notification_request import TNotificationRequest


class NotifierStrategy(Protocol, Generic[TNotificationRequest]):
    async def send_notification(self, request: TNotificationRequest) -> None: ...
