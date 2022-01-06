import time
from minimalub.MinUB import PREFIXES
from . import MinUB, edit_or_reply
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("ping", prefixes=PREFIXES))
@MinUB()
async def ping_cmd(client: Client, message: Message, data: dict):
    st = time.time()
    x = await edit_or_reply(message, "Ping!!!")
    et = time.time()
    x.edit_text(f"Pong!!!\n{(et-st)*100}ms")