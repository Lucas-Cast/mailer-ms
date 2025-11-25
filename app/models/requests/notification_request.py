from typing import Literal, TypeVar
from pydantic import NameEmail
from app.core.base_models import CamelCaseModel
from app.core.constants import DEFAULT_MAIL_PORT, DEFAULT_MAIL_SERVICE
from app.models.enums.notification_type_enum import NotificationTypeEnum


class BaseNotificationRequest(CamelCaseModel):
    recipient: NameEmail
    subject: str
    body: str


class EmailNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.EMAIL]

    mail_server: str = DEFAULT_MAIL_SERVICE
    mail_port: int = DEFAULT_MAIL_PORT
    mail_from_name: str


class SMSNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.SMS]

    phone_number: str
    provider: str


TNotificationRequest = TypeVar(
    "TNotificationRequest", bound=BaseNotificationRequest, contravariant=True
)


SendNotificationPayload = EmailNotificationRequest | SMSNotificationRequest
