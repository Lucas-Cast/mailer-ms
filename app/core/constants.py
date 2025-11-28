from app.core.settings import env_variables

DEFAULT_MAIL_SERVICE = "smtp.gmail.com"
DEFAULT_MAIL_PORT = 587

NOTIFICATION_QUEUE = "notification_queue"
NOTIFICATION_QUEUE_MAX_RETRIES = env_variables.notification_queue_max_retries

DEAD_LETTER_EXCHANGE = f"{NOTIFICATION_QUEUE}_dlx"
DEAD_LETTER_QUEUE = f"{NOTIFICATION_QUEUE}_dlq"
DEAD_LETTER_QUEUE_MAX_RETRIES = env_variables.dead_letter_queue_max_retries

BROKER_URL = env_variables.broker_url
