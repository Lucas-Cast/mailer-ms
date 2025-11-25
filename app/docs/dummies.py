from pydantic import NameEmail
from app.models.enums.notification_type_enum import NotificationTypeEnum
from app.models.requests.notification_request import (
    EmailNotificationRequest,
    SMSNotificationRequest,
)

recipient_dummy = NameEmail(email="email@example", name="Example User")

email_notification_dummy = EmailNotificationRequest(
    type=NotificationTypeEnum.EMAIL,
    recipient=recipient_dummy,
    subject="Subject Example",
    body="Email body content...",
    mail_from_name="System Admin",
).model_dump(by_alias=True)

sms_notification_dummy = SMSNotificationRequest(
    type=NotificationTypeEnum.SMS,
    recipient=recipient_dummy,
    subject="Warning",
    body="Your code is 1234",
    phone_number="+5511999999999",
    provider="Twilio",
).model_dump(by_alias=True)
