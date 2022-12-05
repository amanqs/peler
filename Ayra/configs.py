# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import sys
import os

from decouple import config
from pyrogram import Client, filters
from pytgcalls import PyTgCalls

try:
    from dotenv import load_dotenv
    
    load_dotenv(".env")
except ImportError:
    pass


class Var:
    # mandatory
    API_ID = (
        int(sys.argv[1]) if len(sys.argv) > 1 else config("API_ID", default=9, cast=int)
    )
    API_HASH = (
        sys.argv[2]
        if len(sys.argv) > 2
        else config("API_HASH", default=None)
    )
    SESSION = sys.argv[3] if len(sys.argv) > 3 else config("SESSION", default=None)
    REDIS_URI = (
        sys.argv[4]
        if len(sys.argv) > 4
        else (config("REDIS_URI", default=None) or config("REDIS_URL", default=None))
    )
    REDIS_PASSWORD = (
        sys.argv[5] if len(sys.argv) > 5 else config("REDIS_PASSWORD", default=None)
    )
    STRING_SESSION2 = (
        sys.argv[6] if len(sys.argv) > 6 else config("STRING_SESSION2", default=None)
    )
    PREFIX = (
        sys.argv[7] if len(sys.argv) > 7 else config("PREFIX", "!")
    )
    SUDO_USERS = (
        sys.argv[8] if len(sys.argv) > 8 else config("SUDO_USERS", "1054295664")
    )
    # extras
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    LOG_CHANNEL = config("LOG_CHANNEL", default=0, cast=int)
    HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
    HEROKU_API = config("HEROKU_API", default=None)
    SUDO = config("SUDO", default=True, cast=bool)
    VC_SESSION = config("VC_SESSION", default=SESSION)
    ADDONS = config("ADDONS", default=True, cast=bool)
    INLINE_PIC = config("INLINE_PIC", default=False, cast=bool)
    VCBOT = config("VCBOT", default=True, cast=bool)
    PMSETTING = config("PMSETTING", default=True, cast=bool)
    PMWARNS = config("PMWARNS", "3")
    DISABLE_PMDEL = config("DISABLE_PMDEL", default=True, cast=bool)
    # for railway
    REDISPASSWORD = config("REDISPASSWORD", default=None)
    REDISHOST = config("REDISHOST", default=None)
    REDISPORT = config("REDISPORT", default=None)
    REDISUSER = config("REDISUSER", default=None)
    # for sql
    DATABASE_URL = config("DATABASE_URL", default=None)
    # for MONGODB users
    MONGO_URI = config("MONGO_URI", default=None)
    
    contact_filter = filters.create(
    lambda _, __, message: (message.from_user and message.from_user.is_contact)
    or message.outgoing
)

bot = Client(STRING_SESSION2, API_ID, API_HASH, plugins=dict(root="main"))
call_py = PyTgCalls(bot)
