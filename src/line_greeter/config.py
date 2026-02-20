from __future__ import annotations

import os
from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    openai_api_key: str = ""
    openai_model: str = "gpt-5.2"

    line_channel_access_token: str = ""
    line_user_id: str = ""

    greeting_style: str = "warm"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-5.2"),
            line_channel_access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN", ""),
            line_user_id=os.getenv("LINE_USER_ID", ""),
            greeting_style=os.getenv("GREETING_STYLE", "warm"),
        )

    def validate_or_raise(self) -> None:
        missing = []
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if not self.line_channel_access_token:
            missing.append("LINE_CHANNEL_ACCESS_TOKEN")
        if not self.line_user_id:
            missing.append("LINE_USER_ID")
        if missing:
            raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    # Cached per process; always created AFTER load_dotenv in that process
    return Settings.from_env()