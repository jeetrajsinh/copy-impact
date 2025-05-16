# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Dict, Any

class Settings(BaseSettings):
    GMGN_API_BASE_URL: str = "https://gmgn.ai/api/v1/wallet_holdings/sol/"
    GMGN_API_HEADERS: Dict[str, Any] = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://gmgn.ai/",
        "Origin": "https://gmgn.ai",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    GMGN_API_PARAMS: Dict[str, Any] = {
        "device_id": "5277980a-ee9c-4be5-ad01-241c2af1909f", # Consider moving to .env if sensitive/dynamic
        "client_id": "gmgn_web_2025.0128.214338",
        "from_app": "gmgn",
        "app_ver": "2025.0128.214338",
        "tz_name": "Asia/Calcutta",
        "tz_offset": "19800",
        "app_lang": "en",
        "limit": "300",
        "orderby": "last_active_timestamp",
        "direction": "desc",
        "showsmall": "true",
        "sellout": "true",
        "tx30d": "true"
    }
    GMGN_BROWSER_IMPERSONATE: str = "chrome120"
    API_CALL_DELAY_SECONDS: float = 1.5 # Delay between gmgn.ai API calls

    # For local development, React typically runs on port 3000
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"] # Add your Vite/React dev port

    class Config:
        env_file = ".env" # Load .env file if it exists
        env_file_encoding = 'utf-8'

settings = Settings()