from dotenv import load_dotenv
import os
from pathlib import Path

# Explicitly load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)
