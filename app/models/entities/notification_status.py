from sqlmodel import Field

from app.core.base_models import BaseSQLModel


class NotificationStatus(BaseSQLModel, table=True):
    id: str | None = Field(primary_key=True, default=None)
    name: str = Field(const=True, unique=True)
