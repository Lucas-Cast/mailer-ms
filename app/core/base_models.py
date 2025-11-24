import re
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel
from sqlalchemy.orm import declared_attr


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, validate_by_alias=True, validate_by_name=True
    )


class BaseSQLModel(SQLModel):
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore
        name = cls.__name__
        snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        return snake_name
