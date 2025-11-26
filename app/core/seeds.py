from asyncio import gather
from sqlalchemy.dialects.postgresql import insert
from app.core.db import async_session_factory
from app.models.entities.notification_type import NotificationType
from app.models.entities.notification_status import NotificationStatus
from app.models.enums.notification_status_enum import NotificationStatusEnum
from app.models.enums.notification_type_enum import NotificationTypeEnum


async def run_seeds():
    async with async_session_factory() as session:
        notif_statuses = [
            {"id": enum.value, "name": enum.value} for enum in NotificationStatusEnum
        ]
        notif_types = [
            {"id": enum.value, "name": enum.value} for enum in NotificationTypeEnum
        ]

        notif_status_stmt = (
            insert(NotificationStatus).values(notif_statuses).on_conflict_do_nothing()
        )
        notif_types_stmt = (
            insert(NotificationType).values(notif_types).on_conflict_do_nothing()
        )

        await gather(session.exec(notif_status_stmt), session.exec(notif_types_stmt))
        await session.commit()
