import time
from .. import PREFIXES
from . import MinUB, edit_or_reply
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("ping", prefixes=PREFIXES))
@MinUB()
async def ping_cmd(client: Client, message: Message, data: dict):
    st = time.time()
    x = await edit_or_reply(client, message, "Ping!!!")
    et = time.time()
    await x.edit_text(f"Pong!!!\n{str((et-st)*100)[:6]}ms")