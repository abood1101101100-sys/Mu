from pyrogram import filters
from pyrogram.types import Message
from handlers import router

@router.message(filters.command("start") & filters.me)
async def start_command(client: Client, message: Message):
    """Start command handler"""
    await message.reply_text(
        "🎵 **Music Bot Started!**\n\n"
        "**Available Commands:**\n"
        "`/play <song name/link>` - Play music\n"
        "`/pause` - Pause music\n"
        "`/resume` - Resume music\n"
        "`/skip` - Skip current song\n"
        "`/stop` - Stop music\n"
        "`/queue` - Show queue",
        parse_mode="markdown"
    )
