from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import List

class Settings(BaseSettings):
    FH_TOKEN: str
    BOT_TOKEN: SecretStr
    CHAT_ID: int
    GEMINI_KEYS: str

    @property
    def gemini_keys_list(self) -> List[str]:
        return [k.strip() for k in self.GEMINI_KEYS.split(",") if k.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
