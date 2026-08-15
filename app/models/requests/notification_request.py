from abc import abstractmethod
from typing import Literal, TypeVar

from pydantic import Field, NameEmail, model_validator

from app.core.base_models import CamelCaseModel
from app.core.constants import DEFAULT_MAIL_PORT, DEFAULT_MAIL_SERVICE
from app.models.enums.notification_type_enum import NotificationTypeEnum


class BaseNotificationRequest(CamelCaseModel):
    template_id: str | None = None
    template_variables: dict[str, str | int | float | bool] | None = None

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

    email_body: str | None = None
    recipient_email: NameEmail
    subject: str | None = None
    mail_server: str = DEFAULT_MAIL_SERVICE
    mail_port: int = DEFAULT_MAIL_PORT
    mail_from_name: str

    @property
    def body(self) -> str:
        return self.email_body or ""

    @property
    def recipient(self) -> NameEmail:
        return self.recipient_email

    @model_validator(mode="after")
    def validate_content(self) -> "EmailNotificationRequest":
        if self.template_id is None and (
            self.email_body is None or self.subject is None
        ):
            raise ValueError("email_body and subject are required without template_id")
        return self


class SMSNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.SMS]

    recipient_phone_number: str = Field(pattern=r"^\+[1-9]\d{1,14}$")
    sms_body: str | None = None

    @property
    def body(self) -> str:
        return self.sms_body or ""

    @property
    def recipient(self) -> str:
        return self.recipient_phone_number

    @model_validator(mode="after")
    def validate_content(self) -> "SMSNotificationRequest":
        if self.template_id is None and self.sms_body is None:
            raise ValueError("sms_body is required without template_id")
        return self


class WhatsappNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.WHATSAPP]

    recipient_phone_number: str = Field(pattern=r"^\+[1-9]\d{1,14}$")
    content_sid: str | None = None
    content_variables: dict[str, str | int] | None = None

    @property
    def body(self) -> str:
        return (self.content_sid or "") + " " + str(self.content_variables or "")

    @property
    def recipient(self) -> str:
        return self.recipient_phone_number

    @model_validator(mode="after")
    def validate_content(self) -> "WhatsappNotificationRequest":
        if self.template_id is None and self.content_sid is None:
            raise ValueError("content_sid is required without template_id")
        return self


class BrevoEmailNotificationRequest(BaseNotificationRequest):
    type: Literal[NotificationTypeEnum.BREVO_EMAIL]

    email_body: str | None = None
    recipient_email: str
    subject: str | None = None

    @property
    def body(self) -> str:
        return self.email_body or ""

    @property
    def recipient(self) -> str:
        return self.recipient_email

    @model_validator(mode="after")
    def validate_content(self) -> "BrevoEmailNotificationRequest":
        if self.template_id is None and (
            self.email_body is None or self.subject is None
        ):
            raise ValueError("email_body and subject are required without template_id")
        return self


TNotificationRequest = TypeVar("TNotificationRequest", bound=BaseNotificationRequest)

SendNotificationPayload = (
    EmailNotificationRequest
    | SMSNotificationRequest
    | WhatsappNotificationRequest
    | BrevoEmailNotificationRequest
)


class MessageBrokerPayload(CamelCaseModel):
    log_id: str
    payload: SendNotificationPayload
