from pyrogram import filters
from pyrogram.types import Message
from handlers import router, queues

@router.message(filters.command("queue") & filters.group)
async def queue_command(client, message: Message):
    """Show queue"""
    chat_id = message.chat.id
    
    if chat_id not in queues or not queues[chat_id]:
        await message.reply("📭 **Queue is empty!**")
        return
    
    queue_text = "🎶 **Queue:**\n\n"
    for i, song in enumerate(queues[chat_id], 1):
        queue_text += f"{i}. `{song['title'][:50]}...`\n"
    
    queue_text += f"\n**Total: {len(queues[chat_id])} songs**"
    
    await message.reply(queue_text, parse_mode="markdown")
