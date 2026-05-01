from fastapi.openapi.models import Example

from app.docs.dummies import (
    brevo_email_notification_dummy,
    email_notification_dummy,
    sms_notification_dummy,
    whatsapp_notification_dummy,
)

send_notification_examples = {
    "Email Example": Example(
        summary="Send Email",
        description="Example payload for sending an Email.",
        value=email_notification_dummy,
    ),
    "SMS Example": Example(
        summary="Send SMS",
        description="Example payload for sending an SMS.",
        value=sms_notification_dummy,
    ),
    "WhatsApp Example": Example(
        summary="Send WhatsApp",
        description="Example payload for sending a WhatsApp message.",
        value=whatsapp_notification_dummy,
    ),
    "Brevo Email Example": Example(
        summary="Send Email via Brevo",
        description="Example payload for sending an Email using Brevo API.",
        value=brevo_email_notification_dummy,
    ),
}
