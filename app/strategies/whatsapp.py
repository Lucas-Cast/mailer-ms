import json

from app.core.settings import env_variables
from app.core.twilio_client import get_async_twilio_client
from app.models.requests.notification_request import WhatsappNotificationRequest
from app.strategies.base import NotifierStrategy

WHATSAPP_SENDER_NUMBER = env_variables.whatsapp_sender_number


class WhatsappStrategy(NotifierStrategy[WhatsappNotificationRequest]):
    async def send_notification(self, request: WhatsappNotificationRequest) -> None:
        async with get_async_twilio_client() as client:
            await client.messages.create_async(
                from_=f"whatsapp:{WHATSAPP_SENDER_NUMBER}",
                content_sid=request.content_sid,
                content_variables=json.dumps(request.content_variables),
                to=f"whatsapp:{request.recipient}",
            )
