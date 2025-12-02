from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from twilio.http.async_http_client import AsyncTwilioHttpClient
from twilio.rest import Client

from app.core.settings import env_variables

TWILIO_AUTH_TOKEN = env_variables.twilio_auth_token
TWILIO_ACCOUNT_SID = env_variables.twilio_account_sid


@asynccontextmanager
async def get_async_twilio_client() -> AsyncGenerator[Client, None]:
    http_client = AsyncTwilioHttpClient()

    async with http_client:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, http_client=http_client)

        yield client
