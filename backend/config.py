from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class SupabaseSettings:
    url: str = os.getenv("SUP_URL")
    key: str = os.getenv("SUP_KEY")

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    supabase_settings: SupabaseSettings = SupabaseSettings()
