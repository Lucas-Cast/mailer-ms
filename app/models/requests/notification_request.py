from abc import abstractmethod
from typing import Literal, TypeVar

from pydantic import Field, NameEmail

from app.core.base_models import CamelCaseModel
from app.core.constants import DEFAULT_MAIL_PORT, DEFAULT_MAIL_SERVICE
from app.models.enums.notification_type_enum import NotificationTypeEnum


class BaseNotificationRequest(CamelCaseModel):
    @property
    @abstractmethod
    def body(self) -> str:
        pass

    @property
    @abstractmethod
    def recipient(self) -> str | NameEmail:
        pass


class EmailNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.EMAIL]

    email_body: str
    recipient_email: NameEmail
    subject: str
    mail_server: str = DEFAULT_MAIL_SERVICE
    mail_port: int = DEFAULT_MAIL_PORT
    mail_from_name: str

    @property
    def body(self) -> str:
        return self.email_body

    @property
    def recipient(self) -> NameEmail:
        return self.recipient_email


class SMSNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.SMS]

    provider: str
    recipient_phone_number: str = Field(pattern=r"^\+[1-9]\d{1,14}$")

    @property
    def body(self) -> str:
        return self.body

    @property
    def recipient(self) -> str:
        return self.recipient_phone_number


class WhatsappNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.WHATSAPP]

    recipient_phone_number: str = Field(pattern=r"^\+[1-9]\d{1,14}$")
    content_sid: str
    content_variables: dict[str, str | int] | None = None

    @property
    def body(self) -> str:
        return self.content_sid + " " + str(self.content_variables or "")

    @property
    def recipient(self) -> str:
        return self.recipient_phone_number


TNotificationRequest = TypeVar(
    "TNotificationRequest", bound=BaseNotificationRequest, contravariant=True
)

SendNotificationPayload = (
    EmailNotificationRequest | SMSNotificationRequest | WhatsappNotificationRequest
)


class MessageBrokerPayload(CamelCaseModel):
    log_id: str
    payload: SendNotificationPayload
