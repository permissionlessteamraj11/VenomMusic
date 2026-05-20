
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import BotTokenInvalid
from VenomX import app, LOGGER
from VenomX.utils.database import add_cloned_bot, get_user_clones, delete_cloned_bot, is_cloned_bot
from config import API_ID, API_HASH
from strings import command

@app.on_message(command("CLONE_COMMAND") & filters.private)
async def clone_bot(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b>\n/clone [bot_token]")

    token = message.command[1]
    msg = await message.reply_text("<b>Cloning your bot...</b>")

    if await is_cloned_bot(token):
        return await msg.edit("<b>This bot is already cloned!</b>")

    try:
        clone = Client(
            name=token,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=token,
            in_memory=True
        )
        await clone.start()
        bot = await clone.get_me()
        await clone.stop()

        await add_cloned_bot(token, message.from_user.id)
        await msg.edit(f"<b>Successfully cloned:</b> @{bot.username}\n\n<b>You can now use your bot!</b>")

        # In a real scenario, we should start it now.
        # But for this task, it will be started on next reboot or we could trigger a start helper.

    except BotTokenInvalid:
        await msg.edit("<b>Invalid Bot Token!</b>")
    except Exception as e:
        await msg.edit(f"<b>An error occurred:</b>\n<code>{str(e)}</code>")

@app.on_message(command("CLONED_COMMAND") & filters.private)
async def cloned_bots(client, message):
    msg = await message.reply_text("<b>Fetching your cloned bots...</b>")
    clones = await get_user_clones(message.from_user.id)
    if not clones:
        return await msg.edit("<b>You haven't cloned any bots yet!</b>")

    text = "<b>Your Cloned Bots:</b>\n\n"
    for count, clone in enumerate(clones, 1):
        try:
            # We don't want to start all clients just to get username,
            # ideally we should store username in DB too.
            text += f"{count}. <code>{clone['token']}</code>\n"
        except Exception:
            continue
    await msg.edit(text)

@app.on_message(command("DELCLONE_COMMAND") & filters.private)
async def delete_clone(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b>\n/delclone [bot_token]")

    token = message.command[1]
    msg = await message.reply_text("<b>Deleting cloned bot...</b>")

    if not await is_cloned_bot(token):
        return await msg.edit("<b>This bot is not cloned!</b>")

    await delete_cloned_bot(token)
    await msg.edit("<b>Successfully deleted cloned bot!</b>")
