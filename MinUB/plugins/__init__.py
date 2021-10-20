import asyncio
from .. import mode, LOG_CHANNEL_ID
if mode == ("DUAL" or "BOT"):
    from .. import bot
    c = bot
else:
    from .. import user
    c = user
from .helper import log
from traceback import format_exc as ec
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
                await c.send_message(LOG_CHANNEL_ID, f"#FLOOD #MinUB\nWaited for {e} seconds")
            except MessageNotModified:
                pass
            except Exception as e:
                err = ec()
                await log(func.__name__, err)
                if type(q) == CallbackQuery:
                    await q.answer("Some error occured\nCheck logs")
                else:
                    await q.reply_text("Error!!!\nCheck logs")
        return wrapper
    return get_func
