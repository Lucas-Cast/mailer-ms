import re
from typing import Generic, Protocol

from app.models.entities.template import Template
from app.models.requests.notification_request import TNotificationRequest


def render_template(
    content: str,
    template: Template,
    variables: dict[str, str | int | float | bool] | None,
) -> str:
    values = variables or {}
    schema = template.variable_schema or {}
    missing = [name for name in schema if name not in values]
    if missing:
        raise ValueError(f"Missing template variables: {', '.join(missing)}")

    return re.sub(
        r"{{\s*([\w.-]+)\s*}}",
        lambda match: str(values.get(match.group(1), match.group(0))),
        content,
    )


class NotifierStrategy(Protocol, Generic[TNotificationRequest]):
    def apply_template(
        self, request: TNotificationRequest, template: Template
    ) -> TNotificationRequest: ...

    async def send_notification(self, request: TNotificationRequest) -> None: ...
