from app.core.settings import env_variables

DEFAULT_MAIL_SERVICE = "smtp.gmail.com"
DEFAULT_MAIL_PORT = 587

QUEUE_NAME = "notification_queue"
BROKER_URL = env_variables.broker_url
