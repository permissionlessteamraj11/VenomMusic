
# All rights reserved.

from VenomX.core.mongo import mongodb

clonedb = mongodb.clonedbots

async def get_cloned_bots():
    bots = []
    async for bot in clonedb.find({"token": {"$exists": True}}):
        bots.append(bot)
    return bots

async def add_cloned_bot(token, user_id):
    await clonedb.update_one(
        {"token": token},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_user_clones(user_id):
    bots = []
    async for bot in clonedb.find({"user_id": user_id}):
        bots.append(bot)
    return bots

async def delete_cloned_bot(token):
    await clonedb.delete_one({"token": token})

async def is_cloned_bot(token):
    bot = await clonedb.find_one({"token": token})
    return True if bot else False

async def get_total_clones():
    return await clonedb.count_documents({})
