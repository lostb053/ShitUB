import asyncio, os
from . import mode, LOG_CHANNEL_ID as lc
if mode == ("DUAL" or "BOT"):
    from . import bot
    c = bot
else:
    from . import user
    c = user

async def log(plugin, text):
    hmsg = "#MinUB"
    hmsg += f"  #{plugin.capitalize()}\n\n"
    msg = hmsg
    msg += text
    if len(msg)<4095:
        await c.send_message(lc, msg)
    else:
        filename = "error.txt"
        with open(filename, "w+") as file:
            file.write(msg)
        await c.send_document(
            lc,
            filename,
            caption=hmsg,
        )
        os.remove(filename)
        return
