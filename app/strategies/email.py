from typing import Any

from fastapi_mail import FastMail, MessageSchema, MessageType

from app.core.email_connection_config_factory import create_email_connection_config
from app.models.entities.template import Template
from app.models.requests.notification_request import EmailNotificationRequest
from app.strategies.base import NotifierStrategy, render_template


class EmailStrategy(NotifierStrategy[EmailNotificationRequest]):
    def apply_template(
        self, request: EmailNotificationRequest, template: Template
    ) -> EmailNotificationRequest:
        variables = request.template_variables
        return request.model_copy(
            update={
                "email_body": render_template(template.body, template, variables),
                "subject": render_template(template.subject, template, variables),
            }
        )

    async def send_notification(self, request: EmailNotificationRequest) -> Any:
        conf = create_email_connection_config(
            mail_port=request.mail_port,
            mail_server=request.mail_server,
            mail_from_name=request.mail_from_name,
        )

        if request.subject is None:
            raise ValueError("Subject is required")

        message = MessageSchema(
            subject=request.subject,
            recipients=[request.recipient],
            body=request.body,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message)
