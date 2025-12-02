from app.models.requests.notification_request import SMSNotificationRequest
from app.strategies.base import NotifierStrategy


class SMSStrategy(NotifierStrategy[SMSNotificationRequest]):
    async def send_notification(self, request: SMSNotificationRequest) -> None:
        return
