from pydantic import NameEmail

from app.models.enums.notification_type_enum import NotificationTypeEnum
from app.models.requests.notification_request import (
    EmailNotificationRequest,
    SMSNotificationRequest,
    WhatsappNotificationRequest,
)

recipient_dummy = NameEmail(email="email@example.com", name="Example User")

email_notification_dummy = EmailNotificationRequest(
    type=NotificationTypeEnum.EMAIL,
    recipient_email=recipient_dummy,
    subject="Subject Example",
    email_body="Email body content...",
    mail_from_name="System Admin",
).model_dump(by_alias=True)

sms_notification_dummy = SMSNotificationRequest(
    type=NotificationTypeEnum.SMS,
    recipient_phone_number="+16302339970",
    sms_body="SMS body content...",
).model_dump(by_alias=True)

whatsapp_notification_dummy = WhatsappNotificationRequest(
    type=NotificationTypeEnum.WHATSAPP,
    recipient_phone_number="+5511999999999",
    content_sid="HXb5b62575e6e4ff6129ad7c8efe1f983e",
    content_variables={"1": "12/1", "2": "3pm"},
).model_dump(by_alias=True)
