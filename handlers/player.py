import yt_dlp
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types.input_stream import AudioPiped
from handlers import router, active_chats, queues, call_client

@router.message(filters.command("play") & filters.group)
async def play_command(client, message: Message):
    """Play music command"""
    chat_id = message.chat.id
    
    if not message.reply_to_message and len(message.command) == 1:
        await message.reply("❌ **Please provide a song name or YouTube link!**\n\n"
                          "Example: `/play song name` or `/play https://youtube.com/watch?v=...`")
        return
    
    query = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else ""
    if message.reply_to_message:
        query = message.reply_to_message.text or ""
    
    await message.reply("🔍 **Searching and loading song...**")
    
    try:
        # Download audio with yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
        
        # Add to queue or play directly
        if chat_id not in queues:
            queues[chat_id] = []
        
        song_info = {
            'title': title,
            'duration': duration,
            'path': f"downloads/{title}.mp3"
        }
        
        queues[chat_id].append(song_info)
        
        if len(queues[chat_id]) == 1:  # First song, play immediately
            await play_next(chat_id, message)
        else:
            await message.reply(f"✅ **Added to queue:**\n`{title}`\n**Position:** {len(queues[chat_id])}")
    
    except Exception as e:
        await message.reply(f"❌ **Error:** {str(e)}")

async def play_next(chat_id, message):
    """Play next song in queue"""
    if chat_id not in queues or not queues[chat_id]:
        return
    
    song = queues[chat_id][0]
    try:
        active_chats[chat_id] = True
        
        # Stream audio
        audio_stream = AudioPiped(song['path'])
        await call_client.change_stream(chat_id, audio_stream)
        
        await message.reply(f"🎵 **Now Playing:**\n`{song['title']}`\n⏱ **Duration:** {song['duration']}s")
        
    except Exception as e:
        await message.reply(f"❌ **Error playing song:** {str(e)}")
        queues[chat_id].pop(0)  # Remove failed song
        await play_next(chat_id, message)

@router.message(filters.command("pause") & filters.group)
async def pause_command(client, message: Message):
    """Pause music"""
    chat_id = message.chat.id
    if chat_id in active_chats:
        await call_client.pause_stream(chat_id)
        await message.reply("⏸ **Music Paused**")
    else:
        await message.reply("❌ **No music is playing!**")

@router.message(filters.command("resume") & filters.group)
async def resume_command(client, message: Message):
    """Resume music"""
    chat_id = message.chat.id
    if chat_id in active_chats:
        await call_client.resume_stream(chat_id)
        await message.reply("▶ **Music Resumed**")
    else:
        await message.reply("❌ **No music is playing!**")

@router.message(filters.command("skip") & filters.group)
async def skip_command(client, message: Message):
    """Skip current song"""
    chat_id = message.chat.id
    if chat_id in queues and queues[chat_id]:
        queues[chat_id].pop(0)
        await play_next(chat_id, message)
        await message.reply("⏭ **Skipped to next song!**")
    else:
        await message.reply("❌ **No songs in queue!**")

@router.message(filters.command("stop") & filters.group)
async def stop_command(client, message: Message):
    """Stop music"""
    chat_id = message.chat.id
    if chat_id in active_chats:
        await call_client.stop_stream(chat_id)
        active_chats.pop(chat_id, None)
        queues.pop(chat_id, None)
        await message.reply("⏹ **Music Stopped**")
    else:
        await message.reply("❌ **No music is playing!**")
