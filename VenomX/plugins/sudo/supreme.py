
from pyrogram import filters
from VenomX import app, LOGGER
from config import OWNER_ID
from strings import command
from VenomX.utils.clone_helper import get_clones
import asyncio

@app.on_message(command("SUPREME_COMMAND") & filters.user(OWNER_ID))
async def supreme_panel(client, message):
    from VenomX.utils.database import get_total_clones
    total_clones = await get_total_clones()
    await message.reply_text(f"<b>Welcome to Supreme Panel</b>\n\n<b>Total Cloned Bots:</b> {total_clones}\n\n<b>Commands:</b>\n/gclonebroadcast [message] - Broadcast to all chats of all cloned bots.")

@app.on_message(filters.command("gclonebroadcast") & filters.user(OWNER_ID))
async def gclone_broadcast(client, message):
    from VenomX.utils.database import get_served_chats
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("<b>Usage:</b>\n/gclonebroadcast [message] or reply to a message.")

    query = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    msg = await message.reply_text("<b>Starting Global Broadcast to all cloned bots...</b>")

    clones = await get_clones()
    if not clones:
        return await msg.edit("<b>No cloned bots are currently running.</b>")

    sent = 0
    failed = 0

    chats = await get_served_chats()

    for bot_id, clone_bot in clones.items():
        for chat in chats:
            try:
                if message.reply_to_message:
                    await message.reply_to_message.copy(chat["chat_id"])
                else:
                    await clone_bot.send_message(chat["chat_id"], query)
                sent += 1
                await asyncio.sleep(0.3)
            except Exception:
                failed += 1
                continue

    await msg.edit(f"<b>Global Broadcast Completed!</b>\n\n<b>Total Sent:</b> {sent}\n<b>Failed:</b> {failed}")
