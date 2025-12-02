from typing import Any

from fastapi_mail import FastMail, MessageSchema, MessageType

from app.core.email_connection_config_factory import create_email_connection_config
from app.models.requests.notification_request import EmailNotificationRequest
from app.strategies.base import NotifierStrategy


class EmailStrategy(NotifierStrategy[EmailNotificationRequest]):
    async def send_notification(self, request: EmailNotificationRequest) -> Any:
        conf = create_email_connection_config(
            mail_port=request.mail_port,
            mail_server=request.mail_server,
            mail_from_name=request.mail_from_name,
        )

        message = MessageSchema(
            subject=request.subject,
            recipients=[request.recipient],
            body=request.body,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message)
