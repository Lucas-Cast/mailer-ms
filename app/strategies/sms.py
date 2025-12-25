from app.core.settings import env_variables
from app.core.twilio_client import get_async_twilio_client
from app.models.requests.notification_request import SMSNotificationRequest
from app.strategies.base import NotifierStrategy

SMS_SENDER_NUMBER = env_variables.sms_sender_number


class SMSStrategy(NotifierStrategy[SMSNotificationRequest]):
    async def send_notification(self, request: SMSNotificationRequest) -> None:
        async with get_async_twilio_client() as client:
            await client.messages.create_async(
                from_=f"{SMS_SENDER_NUMBER}",
                to=f"{request.recipient}",
                body=request.sms_body,
            )
