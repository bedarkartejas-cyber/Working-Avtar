import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Explicitly load .env for local development
load_dotenv()

@dataclass(frozen=True)
class Config:
    # LiveKit
    LIVEKIT_URL: str = os.getenv("LIVEKIT_URL", "")
    LIVEKIT_API_KEY: str = os.getenv("LIVEKIT_API_KEY", "")
    LIVEKIT_API_SECRET: str = os.getenv("LIVEKIT_API_SECRET", "")
    
    # Anam
    ANAM_API_KEY: str = os.getenv("ANAM_API_KEY", "")
    ANAM_AVATAR_ID: str = os.getenv("ANAM_AVATAR_ID", "")
    
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    def validate(self):
        missing = [k for k, v in self.__dict__.items() if not v]
        if missing:
            raise ValueError(f"❌ Missing mandatory environment variables: {', '.join(missing)}")

# Create the instance
_config = Config()
_config.validate()

# Export variables as constants so app/api/routes.py can find them
LIVEKIT_URL = _config.LIVEKIT_URL
LIVEKIT_API_KEY = _config.LIVEKIT_API_KEY
LIVEKIT_API_SECRET = _config.LIVEKIT_API_SECRET
ANAM_API_KEY = _config.ANAM_API_KEY
ANAM_AVATAR_ID = _config.ANAM_AVATAR_ID
GEMINI_API_KEY = _config.GEMINI_API_KEY