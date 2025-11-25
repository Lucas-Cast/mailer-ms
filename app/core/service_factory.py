from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_async_session
from app.services.notification_service import NotificationService


def create_service(
    session: AsyncSession = Depends(get_async_session),
) -> NotificationService:
    return NotificationService(session)
