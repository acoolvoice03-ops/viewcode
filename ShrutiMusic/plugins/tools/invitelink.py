# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# All rights reserved.

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired, PeerIdInvalid
from pyrogram.types import Message
from ShrutiMusic import app
from ShrutiMusic.misc import SUDOERS


# =========================
# LEAVE CHAT COMMAND
# =========================
@app.on_message(filters.command("leave") & SUDOERS)
async def leave(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɢʀᴏᴜᴘ ɪᴅ.\nᴜsᴀɢᴇ: `/leave chat_id`"
        )

    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ.")

    msg = await message.reply_text("ʟᴇᴀᴠɪɴɢ ᴄʜᴀᴛ...")

    try:
        await app.send_message(chat_id, "ʟᴇғᴛɪɴɢ ᴄʜᴀᴛ... 👋")
        await app.leave_chat(chat_id)
        await msg.edit(f"✅ ʟᴇғᴛ ᴄʜᴀᴛ `{chat_id}`")
    except Exception:
        await msg.edit("❌ ғᴀɪʟᴇᴅ ᴛᴏ ʟᴇᴀᴠᴇ ᴄʜᴀᴛ.")


# =========================
# GIVE LINK (CURRENT CHAT)
# =========================
@app.on_message(filters.command("givelink"))
async def give_link_command(_, message: Message):
    try:
        link = await app.export_chat_invite_link(message.chat.id)
        await message.reply_text(f"🔗 ɪɴᴠɪᴛᴇ ʟɪɴᴋ:\n{link}")
    except ChatAdminRequired:
        await message.reply_text("❌ ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʀᴇᴀᴛᴇ ʟɪɴᴋ.")
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await message.reply_text("⏳ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
    except Exception:
        await message.reply_text("❌ ᴄᴏᴜʟᴅ ɴᴏᴛ ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋ.")


# =========================
# LINK BY GROUP ID
# =========================
@app.on_message(
    filters.command(
        ["link", "invitelink"],
        prefixes=["/", "!", "%", ",", ".", "@", "#"]
    ) & SUDOERS
)
async def link_command_handler(client: Client, message: Message):

    if len(message.command) != 2:
        return await message.reply_text(
            "❌ ɪɴᴠᴀʟɪᴅ ᴜsᴀɢᴇ.\nᴜsᴇ: `/link group_id`"
        )

    try:
        group_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ɢʀᴏᴜᴘ ɪᴅ.")

    file_name = f"group_info_{group_id}.txt"

    try:
        chat = await client.get_chat(group_id)

        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except ChatAdminRequired:
            invite_link = "Bot is not admin."
        except FloodWait as e:
            await asyncio.sleep(e.x)
            invite_link = "FloodWait occurred."

        group_data = {
            "ID": chat.id,
            "TYPE": str(chat.type),
            "TITLE": chat.title,
            "MEMBERS": chat.members_count,
            "DESCRIPTION": chat.description,
            "INVITE_LINK": invite_link,
            "DC_ID": chat.dc_id,
            "VERIFIED": chat.is_verified,
        }

        with open(file_name, "w", encoding="utf-8") as f:
            for k, v in group_data.items():
                f.write(f"{k}: {v}\n")

        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=f"📄 ɢʀᴏᴜᴘ ɪɴғᴏ\n{chat.title}\n\nᴘᴏᴡᴇʀᴇᴅ ʙʏ @{app.username}",
        )

    except PeerIdInvalid:
        await message.reply_text("❌ ʙᴏᴛ ʜᴀs ɴᴏᴛ ɪɴᴛᴇʀᴀᴄᴛᴇᴅ ᴡɪᴛʜ ᴛʜɪs ɢʀᴏᴜᴘ.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)


__MODULE__ = "Gʀᴏᴜᴘ Lɪɴᴋ"
__HELP__ = """
- `/givelink` : Gᴇᴛ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ᴏғ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ
- `/link group_id` : Gᴇᴛ ɢʀᴏᴜᴘ ɪɴғᴏ + ɪɴᴠɪᴛᴇ ʟɪɴᴋ
"""
