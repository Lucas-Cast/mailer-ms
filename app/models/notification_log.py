from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from app.core.base_models import BaseSQLModel
from app.models.notification_status import NotificationStatus


class NotificationLog(BaseSQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    recipient: str
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    notification_status_id: UUID = Field(foreign_key="notification_status.id")
    notification_status: NotificationStatus = Relationship(
        back_populates="notification_logs"
    )
