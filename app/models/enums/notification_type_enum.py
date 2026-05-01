from enum import StrEnum


class NotificationTypeEnum(StrEnum):
    EMAIL = "Email"
    BREVO_EMAIL = "BrevoEmail"
    SMS = "SMS"
    WHATSAPP = "WhatsApp"
