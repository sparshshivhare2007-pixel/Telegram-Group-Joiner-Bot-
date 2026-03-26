import re
import asyncio
from pyrogram.errors import FloodWait
from config import JOIN_DELAY, MAX_RETRIES

def extract_invite_code(link):
    """Extract invite code from various Telegram link formats"""
    patterns = [
        r'(?:https?://)?(?:www\.)?t\.me/(?:joinchat/)?([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?telegram\.me/(?:joinchat/)?([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?telegram\.dog/(?:joinchat/)?([a-zA-Z0-9_-]+)',
        r'(?:https?://)?t\.me/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?t\.me/\+([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    return None

def extract_all_links(text):
    """Extract all Telegram links from text"""
    link_pattern = r'https?://(?:t\.me|telegram\.me|telegram\.dog)[^\s]+'
    links = re.findall(link_pattern, text)
    return links

async def join_group_with_retry(client, invite_code, retry_count=0):
    """Join group with retry logic"""
    try:
        await client.join_chat(invite_code)
        return True, "Successfully joined"
    except FloodWait as e:
        wait_time = e.value
        await asyncio.sleep(wait_time)
        if retry_count < MAX_RETRIES:
            return await join_group_with_retry(client, invite_code, retry_count + 1)
        return False, f"Flood wait {wait_time}s"
    except Exception as e:
        if retry_count < MAX_RETRIES:
            await asyncio.sleep(JOIN_DELAY)
            return await join_group_with_retry(client, invite_code, retry_count + 1)
        return False, str(e)

def format_progress(current, total, success, failed):
    """Format progress message"""
    percentage = (current / total) * 100 if total > 0 else 0
    return (
        f"🔄 **Progress:** {current}/{total} ({percentage:.1f}%)\n"
        f"✅ **Success:** {success}\n"
        f"❌ **Failed:** {failed}\n"
        f"📊 **Rate:** {success}/{current} successful"
    )

def format_final_results(results, success_count, failed_count):
    """Format final results message"""
    message = (
        f"📊 **Join Summary**\n\n"
        f"✅ **Successfully joined:** {success_count}\n"
        f"❌ **Failed:** {failed_count}\n"
        f"📝 **Total:** {success_count + failed_count}\n\n"
        f"**Details:**\n"
    )
    
    # Add first 15 results
    for result in results[:15]:
        message += f"{result}\n"
    
    if len(results) > 15:
        message += f"\n... and {len(results) - 15} more results"
    
    return message
