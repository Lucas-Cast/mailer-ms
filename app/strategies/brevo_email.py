import httpx

from app.core.settings import env_variables
from app.models.requests.notification_request import BrevoEmailNotificationRequest
from app.strategies.base import NotifierStrategy


class BrevoEmailStrategy(NotifierStrategy[BrevoEmailNotificationRequest]):
    async def send_notification(self, request: BrevoEmailNotificationRequest) -> None:
        headers = {
            "api-key": env_variables.brevo_api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "sender": {
                "email": env_variables.mail_username,
            },
            "to": [{"email": request.recipient_email}],
            "subject": request.subject,
            "htmlContent": request.email_body,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                env_variables.brevo_api_url, json=payload, headers=headers
            )
            response.raise_for_status()
