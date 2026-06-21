from pydantic import Field

from app.core.base_models import CamelCaseModel
from app.models.enums.notification_type_enum import NotificationTypeEnum


class CreateTemplateRequest(CamelCaseModel):
    name: str
    description: str | None
    subject: str
    body: str
    variable_schema: dict[str, str] | None = Field(default=None)
    is_active: bool = Field(default=True)

    notification_type_id: str = Field(default=NotificationTypeEnum.EMAIL)


class UpdateTemplateRequest(CamelCaseModel):
    name: str | None
    description: str | None
    subject: str | None
    body: str | None
    variable_schema: dict[str, str] | None
    is_active: bool | None

    notification_type_id: str | None
