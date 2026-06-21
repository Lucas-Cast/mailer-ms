from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.entities.template import Template
from app.models.requests.template_request import CreateTemplateRequest
from app.services.template_service import TemplateService

router: APIRouter = APIRouter()


@router.post("/")
async def create_template(
    payload: CreateTemplateRequest,
    template_service: Annotated[TemplateService, Depends()],
) -> Template:
    return await template_service.create_template(payload)
