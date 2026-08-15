from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import JSON, Column
from sqlmodel import DateTime, Field, Relationship

from app.core.base_models import BaseSQLModel
from app.models.entities.notification_type import NotificationType


class Template(BaseSQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(const=True)
    description: str | None = Field(default=None)
    subject: str
    body: str
    variable_schema: dict[str, str] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(UTC)
        ),
    )

    notification_type_id: str = Field(foreign_key="notification_type.id")
    notification_type: NotificationType = Relationship()
