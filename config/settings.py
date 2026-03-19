"""
Configuration module for Quiz Bot
Loads environment variables and provides settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
_admin_id_raw = os.getenv("ADMIN_ID")
ADMIN_ID = int(_admin_id_raw) if _admin_id_raw else None

# Database configuration
DATABASE_PATH = "quiz_system.db"

# Validate required settings
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
if not ADMIN_ID:
    raise ValueError("ADMIN_ID not found in .env file")
