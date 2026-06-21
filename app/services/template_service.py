from fastapi import Depends
from sqlalchemy import update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_async_session
from app.models.entities.template import Template
from app.models.requests.template_request import (
    CreateTemplateRequest,
    UpdateTemplateRequest,
)


class TemplateService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
    ):
        self._session = session

    async def create_template(self, payload: CreateTemplateRequest) -> Template:
        template_entity = Template(
            name=payload.name,
            description=payload.description,
            subject=payload.subject,
            body=payload.body,
            variable_schema=payload.variable_schema,
            notification_type_id=payload.notification_type_id,
        )

        self._session.add(template_entity)
        await self._session.commit()
        return template_entity

    async def update_template(
        self,
        template_id: str,
        payload: UpdateTemplateRequest,
    ) -> Template:
        data = payload.model_dump(exclude_unset=True)

        statement = (
            update(Template)
            .where(Template.id == template_id)  # type: ignore
            .values(**data)
        )

        await self._session.exec(statement)
        await self._session.commit()
        return Template(id=template_id, **data)
