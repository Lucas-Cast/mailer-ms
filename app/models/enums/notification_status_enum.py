from enum import StrEnum


class NotificationStatusEnum(StrEnum):
    PENDING = "Pending"
    SENT = "Sent"
    FAILED = "Failed"
