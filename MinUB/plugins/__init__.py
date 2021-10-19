import asyncio
from .. import bot, LOG_CHANNEL_ID
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait, MessageNotModified

def MinUB(owner_only = False, log_sudo = True, log_success = False):
    def get_func(func):
        async def wrapper(_, q):
            if type(q) == Message:
                ...
            if type(q) == CallbackQuery:
                ...
            try:
                await func(_, q)
            except FloodWait as e:
                await asyncio.sleep(e.x+5)
                await bot.send_message(LOG_CHANNEL_ID, f"#FLOOD #MinUB\nWaited for {e} seconds")
            except MessageNotModified:
                pass
            except Exception as e:
                pass
        return wrapper
    return get_func
