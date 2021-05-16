import os
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID")
OWNER_ID = os.environ.get("OWNER_ID")


@Client.on_message(filters.command('start') & filters.incoming & filters.private)
async def start(c, m, cb=False):
    owner = await c.get_users(int(OWNER_ID))
    owner_username = owner.username if owner.username else 'mantapvids'

    # start text
    text = f"""Hey! {m.from_user.mention(style='md')}
💡 ** I am Family File Storage Bot**
`You can store your Telegram Media for permanent Link!`
"""

    # Buttons
    buttons = [
        [
            InlineKeyboardButton('My Channel', url=f"https://t.me/FStorage"),
            InlineKeyboardButton('Help 💡', callback_data="help")
        ],
        [
            InlineKeyboardButton('About 📕', callback_data="about")
        ]
    ]

    # when button home is pressed
    if cb:
        return await m.message.edit(
                   text=text,
                   reply_markup=InlineKeyboardMarkup(buttons)
               )

    if len(m.command) > 1: # sending the stored file
        chat_id, msg_id = m.command[1].split('_')
        msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

        if msg.empty:
            owner = await c.get_users(int(OWNER_ID))
            return await m.reply_text(f"🥴 Sorry bro your file was missing\n\nPlease contact my owner 👉 {owner.mention(style='md')}")
        
        caption = f"{msg.caption.markdown}\n\n\n" if msg.caption else ""

        if chat_id.startswith('-100'): #if file from channel
            channel = await c.get_chat(int(chat_id))
            caption += "**TUTORIAL DOWNLOAD**\n\n"
            caption += f"__Untuk menonton video silahkan Klik **download** lalu klik **start** untuk menonton video atau file__\n\n"
            caption += f"__📢 Channel Name:__ `{m.chat.title}`\n\n"
            caption += f"@FamilyStorageBot\n\n”
            caption += f"__👁 Members Count:__ {m.chat.members_count}\n\n" if m.chat.members_count else ""

        else: #if file not from channel
            user = await c.get_users(int(chat_id))
            caption += "**TUTORIAL DOWNLOAD**\n\n"
            caption += f"__Untuk menonton video silahkan Klik **download** lalu klik **start** untuk menonton video atau file__\n\n"
            caption += f"__📢 Channel Name:__ `{m.chat.title}`\n\n"
            caption += f"@FamilyStorageBot\n\n"

        await msg.copy(m.from_user.id, caption=caption)


    else: # sending start message
        await m.reply_text(
            text=text,
            quote=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@Client.on_message(filters.command('me') & filters.incoming & filters.private)
async def me(c, m):
    me = await c.get_users(m.from_user.id)
    text = "--**YOUR DETAILS:**--\n\n\n"
    text += f"__🦚 First Name:__ `{me.first_name}`\n\n"
    text += f"__🐧 Last Name:__ `{me.last_name}`\n\n" if me.last_name else ""
    text += f"__👁 User Name:__ @{me.username}\n\n" if me.username else ""
    text += f"__✔ Is Verified By TELEGRAM:__ `{me.is_verified}`\n\n" if me.is_verified else ""
    text += f"__👺 Is Fake:__ {me.is_fake}\n\n" if me.is_fake else ""
    text += f"__💨 Is Scam:__ {me.is_scam}\n\n" if me.is_scam else ""
    text += f"__📃 Language Code:__ {me.language_code}\n\n" if me.language_code else ""

    await m.reply_text(text, quote=True)
