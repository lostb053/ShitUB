import asyncio
import json

from anibot.anibot import BOT_TOKEN, OWNER
from .. import mode, LOG_CHANNEL_ID
if mode == ("DUAL" or "BOT"):
    from .. import bot
    c = bot
else:
    from .. import user
    c = user
from ._helper import log
from traceback import format_exc as ec
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait, MessageNotModified

ALL_USERS = []

def MinUB(owner_only = False, log_sudo = True, log_success = False):
    def get_func(func):
        async def wrapper(_, q):
            data = json.loads(str(q))
            if type(q) == Message:
                q: Message = q
                if owner_only and (q.from_user.id not in OWNER):
                    return
                if log_sudo:
                    await log(func.__name__, f"Sudo user {q.from_user.id} used the following command\n\n`{q.text}`")
                if q.from_user.id not in ALL_USERS:
                    return
                if q.text.pop()==".":
                    if (q.from_user.id not in OWNER):
                        return
                    client = user
                else:
                    try:
                        await user.get_chat_member(q.chat.id, BOT_TOKEN.split(":")[0])
                    except Exception:
                        ...
            if type(q) == CallbackQuery:
                q: CallbackQuery = q
            try:
                await func(_, q, data)
                if log_success:
                    await log(func.__name__, f"Following command executed succesfully\n\n`{q.text}`")
            except FloodWait as e:
                await asyncio.sleep(e.x+5)
                await log("FLOOD", f"Waited for {e} seconds")
            except MessageNotModified:
                pass
            except Exception as e:
                err = ec()
                await log(func.__name__, err)
                if type(q) == CallbackQuery:
                    await q.answer("Some error occured\nCheck logs", show_alert=True)
                else:
                    await q.reply_text("Error!!!\nCheck logs")
        return wrapper
    return get_func
