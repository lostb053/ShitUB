import asyncio
from . import mode
from pyrogram import idle

if mode == "ERROR":
    print("No user session or bot token given!!!")
    exit()

clients = []

async def main():
    if mode == "DUAL":
        from . import bot, user
        clients.append(bot, user)
    if mode == "BOT":
        from . import bot
        clients.append(bot)
    if mode == "USER":
        from . import user
        clients.append(user)
    asyncio.gather(i.start() for i in clients)
    idle()
    asyncio.gather(i.stop() for i in clients)

asyncio.get_event_loop().run_until_complete(main())