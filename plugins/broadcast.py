# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.


from . import get_help

__doc__ = get_help("help_broadcast")

import asyncio
import io

from telethon.utils import get_display_name

from Ayra.dB.broadcast_db import *

from . import HNDLR, LOGS, ayra_bot, ayra_cmd, eor, get_string, udB


@ayra_cmd(
    pattern="addch( (.*)|$)",
    allow_sudo=False,
)
async def broadcast_adder(event):
    msgg = event.pattern_match.group(1).strip()
    x = await event.eor(get_string("bd_1"))
    if msgg == "all":
        await x.edit(get_string("bd_2"))
        chats = [
            e.entity
            for e in await event.client.get_dialogs()
            if (e.is_group or e.is_channel)
        ]
        new = 0
        for i in chats:
            try:
                if (
                    i.broadcast
                    and (i.creator or i.admin_rights)
                    and not is_channel_added(i.id)
                ):
                    new += 1
                    cid = f"-100{i.id}"
                    add_channel(int(cid))
            except Exception as Ex:
                LOGS.exception(Ex)
        await x.edit(get_string("bd_3").format(get_no_channels(), new))
        return
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        raw_text = previous_message.text
        lines = raw_text.split("\n")
        length = len(lines)
        for line_number in range(1, length - 2):
            channel_id = lines[line_number][4:-1]
            if not is_channel_added(channel_id):
                add_channel(channel_id)
        await x.edit(get_string("bd_4"))
        await asyncio.sleep(3)
        await event.delete()
        return
    chat_id = event.chat_id
    if chat_id == udB.get_key("LOG_CHANNEL"):
        return
    if is_channel_added(chat_id):
        await x.edit(get_string("bd_6"))
    elif xx := add_channel(chat_id):
        await x.edit(get_string("bd_5"))
    else:
        await x.edit(get_string("sf_8"))
    await asyncio.sleep(3)
    await x.delete()


@ayra_cmd(
    pattern="remch( (.*)|$)",
    allow_sudo=False,
)
async def broadcast_remover(event):
    chat_id = event.pattern_match.group(1).strip() or event.chat_id
    x = await event.eor(get_string("com_1"))
    if chat_id == "all":
        await x.edit(get_string("bd_8"))
        udB.del_key("BROADCAST")
        await x.edit("Basis data dihapus.")
        return
    if is_channel_added(chat_id):
        rem_channel(chat_id)
        await x.edit(get_string("bd_7"))
    else:
        await x.edit(get_string("bd_9"))
    await asyncio.sleep(3)
    await x.delete()


@ayra_cmd(
    pattern="listchannels$",
)
async def list_all(event):
    x = await event.eor(get_string("com_1"))
    channels = get_channels()
    num = len(channels)
    if not channels:
        return await eor(x, "Tidak ada obrolan yang ditambahkan.", time=5)
    msg = "Saluran dalam database:\n"
    for channel in channels:
        name = ""
        try:
            name = get_display_name(await event.client.get_entity(channel))
        except ValueError:
            name = ""
        msg += f"=> **{name}** [`{channel}`]\n"
    msg += f"\nTotal {num} channels."
    if len(msg) > 4096:
        MSG = msg.replace("*", "").replace("`", "")
        with io.BytesIO(str.encode(MSG)) as out_file:
            out_file.name = "channels.txt"
            await event.reply(
                "Saluran di Database",
                file=out_file,
                force_document=True,
                allow_cache=False,
            )
            await x.delete()
    else:
        await x.edit(msg)


@ayra_cmd(
    pattern="forward$",
    allow_sudo=False,
)
async def forw(event):
    if not event.is_reply:
        return await event.eor(get_string("ex_1"))
    ayra_bot = event.client
    channels = get_channels()
    x = await event.eor("Mengirim...")
    if not channels:
        return await x.edit(
            f"Tambahkan saluran dengan menggunakan `{HNDLR}add` in them."
        )
    error_count = 0
    sent_count = 0
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
    error_count = 0
    for channel in channels:
        try:
            await ayra_bot.forward_messages(channel, previous_message)
            sent_count += 1
            await x.edit(
                f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}",
            )
        except Exception:
            try:
                await ayra_bot.send_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    f"Kesalahan dalam mengirim di {channel}.",
                )
            except Exception as Em:
                LOGS.info(Em)
            error_count += 1
            await x.edit(
                f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}",
            )
    await x.edit(f"{sent_count} messages sent with {error_count} errors.")
    if error_count > 0:
        await ayra_bot.send_message(
            int(udB.get_key("LOG_CHANNEL")), f"{error_count} Errors"
        )


@ayra_cmd(
    pattern="broadcast( (.*)|$)",
    allow_sudo=False,
)
async def sending(event):
    x = await event.eor(get_string("com_1"))
    if not event.is_reply:
        return await x.edit(get_string("ex_1"))
    channels = get_channels()
    if not channels:
        return await x.edit(
            f"Tambahkan saluran dengan menggunakan `{HNDLR}add` in them."
        )
    await x.edit("Mengirim....")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.poll:
            return await x.edit(f"Reply `{HNDLR}forward` for polls.")
        if previous_message:
            error_count = 0
            sent_count = 0
            for channel in channels:
                try:
                    await ayra_bot.send_message(channel, previous_message)
                    sent_count += 1
                    await x.edit(
                        f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}",
                    )
                except Exception as error:

                    await ayra_bot.send_message(
                        udB.get_key("LOG_CHANNEL"),
                        f"Error in sending at {channel}.\n\n{error}",
                    )
                    error_count += 1
                    await x.edit(
                        f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}",
                    )
            await x.edit(f"{sent_count} messages sent with {error_count} errors.")
            if error_count > 0:
                await ayra_bot.send_message(
                    int(udB.get_key("LOG_CHANNEL")),
                    f"{error_count} Errors",
                )
