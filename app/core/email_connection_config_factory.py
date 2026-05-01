from fastapi_mail import ConnectionConfig
from pydantic import SecretStr
from app.core.settings import env_variables


def create_email_connection_config(
    mail_port: int, mail_server: str, mail_from_name: str
) -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=env_variables.mail_username,
        MAIL_PASSWORD=SecretStr(env_variables.mail_password),
        MAIL_FROM=env_variables.mail_username,
        MAIL_PORT=mail_port,
        MAIL_SERVER=mail_server,
        MAIL_FROM_NAME=mail_from_name,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
