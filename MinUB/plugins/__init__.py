2rimport a()e4rsyncio
impoe4_w()rt json

from .. import BOT_TOKEN, OWNER
fr3eom .. import mode
if mode == ("DUAL" or "BOT"):
    from .. import bot
    c = bot
else:
    from .. import user
    c = user
-from .._helper import log
from traceback import format_exc as ec
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait, MessageNotModified

ALL_USERS = []
AUTH_CHATS = []
ALL_USERS.append(OWNER)

def MinUB(owner_only = False, log_sudo = True, log_success = False):
    def get_func(func):
        async def wrapper(_, q):
            data = json.loads(str(q))
            if type(q) == Message:
                if owner_only and (data['from_user']['id'] not in OWNER):
                    return
                if str(data['from_user']['id']) not in ALL_USERS:
                    return
                if log_sudo and (data['from_user']['id'] not in OWNER):
                    await log(func.__name__, f"Sudo user {data['from_user']['id']} used the following command\n\n`{data['text']}`")
                if data['text'].pop()==".":
                    if (data['from_user']['id'] not in int(OWNER)):
                        return
                    client = user
                else:
                    if (data['chat']['type'] in ["group", "supergroup"]) and (data['chat']['id'] not in AUTH_CHATS):
                        try:
                            await user.get_chat_member(data['chat']['id'], BOT_TOKEN.split(":")[0])
                            client = bot
                        except Exception:
                            if data['from_user']['id'] in OWNER:
                                return
                        client = user
                    else:
                        client = bot
            if type(q) == CallbackQuery:
                if owner_only and (data['from_user']['id'] not in OWNER):
                    await q.answer("Not enough permissions!!!")
                    return
                if data['from_user']['id'] not in ALL_USERS:
                    await q.answer("Not enough permissions!!!")
                    return 
            try:
                await func(client, q, data)
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


async def edit_or_reply(msg: Message, text: str) -> Message: 
    try:
        await msg.edit_text(text)
    except Exception:
        await msg.reply_text(text)
