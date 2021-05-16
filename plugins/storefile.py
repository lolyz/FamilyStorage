


import os
import urllib
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID")



#################################### FOR PRIVATE ################################################
@Client.on_message((filters.document|filters.video|filters.audio|filters.photo) & filters.incoming & ~filters.edited & ~filters.channel)
async def storefile(c, m):

    if m.document:
       media = m.document
    if m.video:
       media = m.video
    if m.audio:
       media = m.audio
    if m.photo:
       media = m.photo

    # text
    text = ""
    if not m.photo:
        text = "@FamilyStorageBot\n\n"

    # if databacase channel exist forwarding message to channel
    if DB_CHANNEL_ID:
        msg = await m.copy(int(DB_CHANNEL_ID))
        await msg.reply(text)

    # creating urls
    bot = await c.get_me()
    url = f"https://t.me/{bot.username}?start={m.chat.id}_{m.message_id}" if not DB_CHANNEL_ID else f"https://t.me/{bot.username}?start={m.chat.id}_{msg.message_id}"
    txt = urllib.parse.quote(text.replace('--', ''))
    share_url = f"tg://share?url={txt}File%20Link%20👉%20{url}"

    # making buttons
    buttons = [[
        InlineKeyboardButton(text="Download Video 🔗", url=url),
        InlineKeyboardButton(text="Share Link 👤", url=share_url)
    ]]

    # sending message
    await m.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

#################################### FOR CHANNEL################################################

@Client.on_message((filters.document|filters.video|filters.audio|filters.photo) & filters.incoming & filters.channel & ~filters.edited)
async def storefile_channel(c, m):

    if m.document:
       media = m.document
    if m.video:
       media = m.video
    if m.audio:
       media = m.audio
    if m.photo:
       media = m.photo

    # text
    text = ""
    if not m.photo:
        text = "@FamilyStorageBot\n\n"
    text += f"__👁 Members Count:__ {m.chat.members_count}\n\n" if m.chat.members_count else ""

    # if databacase channel exist forwarding message to channel
    if DB_CHANNEL_ID:
        msg = await m.copy(int(DB_CHANNEL_ID))
        await msg.reply(text)

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
        ((str(hours) + " hrs, ") if hours else "") + \
        ((str(minutes) + " min, ") if minutes else "") + \
        ((str(seconds) + " sec, ") if seconds else "") + \
        ((str(milliseconds) + " millisec, ") if milliseconds else "")
    return tmp[:-2]
