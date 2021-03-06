import asyncio
import json

from .. import BOT_TOKEN, OWNER
from .. import mode
if mode=="DUAL":
    from .. import bot, user
elif mode=="BOT":
    from .. import bot
else:
    from .. import user
from .._helper import log
from traceback import format_exc as ec
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait, MessageNotModified

ALL_USERS = []
AUTH_CHATS = []
ALL_USERS = ALL_USERS + OWNER

def MinUB(owner_only = False, log_sudo = True, log_success = False):
    def get_func(func):
        async def wrapper(_, q):
            print("1")
            data = json.loads(str(q))
            if type(q) == Message:
                if owner_only and (data['from_user']['id'] not in OWNER):
                    print("2")
                    return
                if data['from_user']['id'] not in ALL_USERS:
                    print("3")
                    return
                if log_sudo and (data['from_user']['id'] not in OWNER):
                    await log(func.__name__, f"Sudo user {data['from_user']['id']} used the following command\n\n`{data['text']}`")
                if data['text'][0]==".":
                    print("9")
                    if (data['from_user']['id'] not in OWNER):
                        print("4")
                        return
                    client = user
                else:
                    print("8")
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
                    print("6")
                    return
                if data['from_user']['id'] not in ALL_USERS:
                    await q.answer("Not enough permissions!!!")
                    print("7")
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


async def edit_or_reply(client: Client, msg: Message, text: str):
    try:
        m = await client.edit_message_text(msg.chat.id, msg.message_id, text)
    except Exception:
        m = await client.send_message(msg.chat.id, text, reply_to_message_id=msg.message_id)
    return m