from dotenv import load_dotenv
from pydantic import BaseModel

from app.utils.get_env_or_throw import get_env_or_throw

load_dotenv()


class Settings(BaseModel):
    pg_url: str = get_env_or_throw("POSTGRES_URL")
    mail_username: str = get_env_or_throw("MAIL_USERNAME")
    mail_password: str = get_env_or_throw("MAIL_PASSWORD")
    broker_url: str = get_env_or_throw("MESSAGE_BROKER_URL")
    notification_queue_max_retries: int = get_env_or_throw(
        "NOTIFICATION_QUEUE_MAX_RETRIES", cast=int
    )
    dead_letter_queue_max_retries: int = get_env_or_throw(
        "DEAD_LETTER_QUEUE_MAX_RETRIES", cast=int
    )
    twilio_account_sid: str = get_env_or_throw("TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = get_env_or_throw("TWILIO_AUTH_TOKEN")
    whatsapp_sender_number: str = get_env_or_throw("WHATSAPP_SENDER_NUMBER")
    sms_sender_number: str = get_env_or_throw("SMS_SENDER_NUMBER")


env_variables = Settings()
