from pydantic import BaseModel
from dotenv import load_dotenv
from app.utils.get_env_or_throw import get_env_or_throw

load_dotenv()


class Settings(BaseModel):
    pg_url: str = get_env_or_throw("POSTGRES_URL")


env_variables = Settings()
