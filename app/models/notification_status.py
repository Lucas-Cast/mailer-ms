from uuid import UUID, uuid4
from sqlmodel import Field

from app.core.base_models import BaseSQLModel


class NotificationStatus(BaseSQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(const=True, unique=True)
