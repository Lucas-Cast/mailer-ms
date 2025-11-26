from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.docs.examples import send_notification_examples
from app.models.requests.notification_request import (
    SendNotificationPayload,
)
from app.services.notification_service import NotificationService

router: APIRouter = APIRouter()


@router.post("/send", response_model=str)
async def send_notification(
    payload: Annotated[
        SendNotificationPayload,
        Body(
            discriminator="type",
            openapi_examples=send_notification_examples,
        ),
    ],
    notification_service: NotificationService = Depends(),
) -> str:
    return await notification_service.publish_notification(payload)
