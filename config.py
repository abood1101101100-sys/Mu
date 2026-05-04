import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API Credentials
API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING", "")  # Optional for userbot

# FFmpeg path (for Replit)
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")

# Bot Settings
OWNER_ID = int(os.getenv("OWNER_ID", "YOUR_USER_ID"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))  # Optional
