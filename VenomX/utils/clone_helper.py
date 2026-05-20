
import asyncio
from pyrogram import Client
from VenomX import LOGGER, app
from VenomX.utils.database import get_cloned_bots
from config import API_ID, API_HASH
from VenomX.plugins import ALL_MODULES
import importlib

clones = {}

async def restart_bots():
    global clones
    LOGGER("VenomX.Clones").info("Restarting cloned bots...")
    bots = await get_cloned_bots()
    for bot_data in bots:
        token = bot_data["token"]
        try:
            clone = Client(
                name=f"clone_{token[:10]}",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=token,
                in_memory=True
            )
            await clone.start()

            # Copy handlers from main app to clone
            for handler in app.dispatcher.groups.values():
                for h in handler:
                    clone.add_handler(h)

            clones[clone.me.id] = clone
            LOGGER("VenomX.Clones").info(f"Started cloned bot: @{clone.me.username}")
        except Exception as e:
            LOGGER("VenomX.Clones").error(f"Failed to start cloned bot {token[:10]}: {str(e)}")

async def get_clones():
    return clones
