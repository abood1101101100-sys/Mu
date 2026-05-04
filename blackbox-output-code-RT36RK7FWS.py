import asyncio
import logging
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING
from handlers import start, player, queue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize clients
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
if SESSION_STRING:
    user_client = Client("userbot", session_string=SESSION_STRING)
else:
    user_client = app

# Initialize PyTgCalls
call_client = PyTgCalls(app, user_client)

@app.on_startup()
async def on_startup():
    """Start the bot"""
    logger.info("Bot is starting...")
    await app.start()
    await call_client.start()
    logger.info("Bot started successfully!")

@app.on_shutdown()
async def on_shutdown():
    """Stop the bot"""
    await call_client.stop()
    await app.stop()
    logger.info("Bot stopped!")

# Register handlers
app.include_router(start.router)
app.include_router(player.router)
app.include_router(queue.router)

if __name__ == "__main__":
    # Install FFmpeg for Replit
    import subprocess
    import sys
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "ffmpeg-python"], 
                      check=True, capture_output=True)
    except:
        pass
    
    asyncio.run(app.idle())