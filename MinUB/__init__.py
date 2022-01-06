import os
from pyrogram import Client

STRIGGERS = os.environ.get("SUDO_TRIGGERS", "/ !").split()
MTRIGGER = os.environ.get("TRIGGER", ".").split()[0]
if MTRIGGER in STRIGGERS:
    STRIGGERS.remove(MTRIGGER)
TRIGGERS = STRIGGERS.append(MTRIGGER)
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_NAME = os.environ.get("BOT_NAME")
DB_URL = os.environ.get("DATABASE_URL")
API_ID = int(os.environ.get("API_ID"))
SESSION = os.environ.get('USER_SESSION')
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID"))
OWNER = list(filter(lambda x: x, map(int, os.environ.get("OWNER_ID", "1005170481 1993696756").split())))
DOWN_PATH = os.environ.get("DOWN_PATH", "MinUB/downloads/")
HELP_DICT = dict()

plugins = dict(root="MinUB/plugins")

if (BOT_TOKEN and SESSION) is None:
    mode = "ERROR"
if BOT_TOKEN is None:
    mode = "USER"
if SESSION is None:
    mode = "BOT"
if (BOT_TOKEN and SESSION) is not None:
    mode = "DUAL"

if mode == "DUAL":
    bot = Client("MinUB", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=plugins)
    user = Client(SESSION , api_id=API_ID, api_hash=API_HASH)
    PREFIXES = [MTRIGGER]+STRIGGERS
elif mode == "BOT":
    bot = Client("MinUB", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=plugins)
    PREFIXES = STRIGGERS
elif mode == "USER":
    user = Client(SESSION , api_id=API_ID, api_hash=API_HASH)
    PREFIXES = MTRIGGER