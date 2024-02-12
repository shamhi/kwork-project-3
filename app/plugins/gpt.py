import random
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
import aiosqlite

from app.db import Database
from app.utils.eden_ai import gpt_response, speech_to_text
from app.utils import scripts


@Client.on_message(~filters.me & filters.private & filters.text)
async def answer_gpt_on_text(client: Client, message: Message, conn: aiosqlite.Connection):
    db = Database(conn=conn)
    text = message.text
    user = message.from_user

    history = await db.get_history_messages(tg_id=user.id)

    await db.register_user(tg_id=user.id, username=str(user.username), firstname=user.first_name)

    await asyncio.sleep(delay=random.randint(3, 10))
    await client.read_chat_history(chat_id=message.chat.id)

    await db.add_message(tg_id=user.id)

    response, messages = await gpt_response(prompt=text, history=history)
    if not response:
        return

    history.extend(messages)
    history = scripts.get_dumped_data(history)
    await db.add_history_messages(tg_id=user.id, history=history)

    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(delay=random.randint(3, 10))

    await message.reply(text=response)


@Client.on_message(~filters.me & filters.private & (filters.voice | filters.audio | filters.video | filters.video_note))
async def answer_gpt_on_speech(client: Client, message: Message, conn: aiosqlite.Connection):
    db = Database(conn=conn)
    user = message.from_user
    media_type = message.media.name.lower()
    duration = scripts.get_media_duration(message=message, media_type=media_type)

    history = await db.get_history_messages(tg_id=user.id)

    await client.read_chat_history(chat_id=message.chat.id)

    path = await client.download_media(message, file_name='downloads/media.mp3')
    file_bytes = scripts.get_file_bytes_by_path(path=path)

    parsed_text = await speech_to_text(file_bytes=file_bytes)

    response, messages = await gpt_response(prompt=parsed_text, history=history)
    if not response:
        return

    history.extend(messages)
    history = scripts.get_dumped_data(history)
    await db.add_history_messages(tg_id=user.id, history=history)

    await asyncio.sleep(delay=duration)
    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    await message.reply(text=response)

    await db.add_message(tg_id=user.id)
