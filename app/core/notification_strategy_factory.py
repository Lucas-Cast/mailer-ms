from typing import cast

from app.models.requests.notification_request import (
    EmailNotificationRequest,
    SMSNotificationRequest,
    TNotificationRequest,
    WhatsappNotificationRequest,
)
from app.strategies.base import NotifierStrategy
from app.strategies.email import EmailStrategy
from app.strategies.sms import SMSStrategy
from app.strategies.whatsapp import WhatsappStrategy


def get_notification_strategy(
    payload: TNotificationRequest,
) -> NotifierStrategy[TNotificationRequest]:
    if isinstance(payload, EmailNotificationRequest):
        return cast(NotifierStrategy[TNotificationRequest], EmailStrategy())

    if isinstance(payload, SMSNotificationRequest):
        return cast(NotifierStrategy[TNotificationRequest], SMSStrategy())

    if isinstance(payload, WhatsappNotificationRequest):
        return cast(NotifierStrategy[TNotificationRequest], WhatsappStrategy())

    raise ValueError(f"Unknown notification type: {type(payload)}")
