from pydantic import NameEmail

from app.models.enums.notification_type_enum import NotificationTypeEnum
from app.models.requests.notification_request import (
    BrevoEmailNotificationRequest,
    EmailNotificationRequest,
    SMSNotificationRequest,
    WhatsappNotificationRequest,
)

recipient_dummy = NameEmail(email="email@example.com", name="Example User")

email_notification_dummy = EmailNotificationRequest(
    type=NotificationTypeEnum.EMAIL,
    template_id="template-id-example",
    template_variables={"nome": "Example User"},
    recipient_email=recipient_dummy,
    subject="Subject Example",
    email_body="Email body content...",
    mail_from_name="System Admin",
).model_dump(by_alias=True)

sms_notification_dummy = SMSNotificationRequest(
    type=NotificationTypeEnum.SMS,
    template_id="template-id-example",
    template_variables={"nome": "Example User"},
    recipient_phone_number="+16302339970",
    sms_body="SMS body content...",
).model_dump(by_alias=True)

whatsapp_notification_dummy = WhatsappNotificationRequest(
    type=NotificationTypeEnum.WHATSAPP,
    template_id="template-id-example",
    template_variables={"nome": "Example User"},
    recipient_phone_number="+5511999999999",
    content_sid="HXb5b62575e6e4ff6129ad7c8efe1f983e",
    content_variables={"1": "12/1", "2": "3pm"},
).model_dump(by_alias=True)

brevo_email_notification_dummy = BrevoEmailNotificationRequest(
    type=NotificationTypeEnum.BREVO_EMAIL,
    template_id="template-id-example",
    template_variables={"nome": "Example User"},
    recipient_email="email@example.com",
    subject="Subject Example",
    email_body="<h1>Email body content...</h1>",
).model_dump(by_alias=True)
