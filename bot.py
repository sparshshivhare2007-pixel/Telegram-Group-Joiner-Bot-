import asyncio
import os
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, JOIN_DELAY
from utils import extract_invite_code, extract_all_links, format_progress, format_final_results, join_group_with_retry
from database import Database

# Initialize bot
app = Client("group_joiner_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = Database()

# Store active join processes
active_joins = {}

@app.on_message(filters.command("start"))
async def start_command(client, message):
    welcome_text = """
🤖 **Telegram Group Joiner Bot**

**Commands:**
• `/add` - Add group links
• `/status` - Check added links
• `/addaccount` - Add user session
• `/join` - Start joining groups
• `/clear` - Clear all links
• `/help` - Show detailed help

**Quick Start:**
1. `/addaccount` - Send your .session file
2. `/add` - Add group links
3. `/join` - Start joining
"""
    await message.reply_text(welcome_text)

@app.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = """
📖 **Detailed Help**

**Adding Account:**
1. Create session file using Pyrogram
2. Send the .session file to bot
3. Reply with `/addaccount`

**How to create session:**
```python
from pyrogram import Client
app = Client('my_session', api_id=YOUR_API_ID, api_hash='YOUR_API_HASH')
app.run()
