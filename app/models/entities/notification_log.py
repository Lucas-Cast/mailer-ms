from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Column
from sqlmodel import DateTime, Field, Relationship

from app.core.base_models import BaseSQLModel
from app.core.settings import env_variables
from app.models.entities.notification_status import NotificationStatus
from app.models.entities.notification_type import NotificationType


class NotificationLog(BaseSQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    recipient: str
    sent_by: str = Field(default=env_variables.mail_username)
    body: str
    error_message: str | None = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True)),
    )

    notification_status_id: str = Field(foreign_key="notification_status.id")
    notification_status: NotificationStatus = Relationship()

    notification_type_id: str = Field(foreign_key="notification_type.id")
    notification_type: NotificationType = Relationship()
