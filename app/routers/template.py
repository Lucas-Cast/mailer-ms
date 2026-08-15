from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.entities.template import Template
from app.models.requests.template_request import (
    CreateTemplateRequest,
    UpdateTemplateRequest,
)
from app.services.template_service import TemplateService

router: APIRouter = APIRouter()


@router.post("/")
async def create_template(
    payload: CreateTemplateRequest,
    template_service: Annotated[TemplateService, Depends()],
) -> Template:
    return await template_service.create_template(payload)


@router.put("/{template_id}")
async def update_template(
    template_id: str,
    payload: UpdateTemplateRequest,
    template_service: Annotated[TemplateService, Depends()],
) -> Template:
    return await template_service.update_template(template_id, payload)
