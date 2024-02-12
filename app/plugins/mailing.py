import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.me & filters.private & filters.command(['mailing', 'message'], prefixes="/"))
async def send_mailing(client: Client, message: Message):
    text = " ".join(message.command[1:])

    if not text:
        return await message.reply(
            text='<emoji id=5210952531676504517>❌</emoji><b>Ты не ввел текст после команды!!!</b>',
            reply_to_message_id=message.id)

    chats = [obj.chat.id async for obj in client.get_dialogs()]
    count = 0

    for chat_id in chats:
        try:
            await client.send_message(chat_id=chat_id, text=text)
            count += 1
            await asyncio.sleep(delay=random.randint(5, 30))
        except Exception as er:
            error_chat = await client.get_chat(chat_id=chat_id)
            print(f"Не удалось отправить сообщение в чат {error_chat.username}\n"
                  f"Ошибка: {er}")

    await message.reply(
        text=f"<emoji id=5206607081334906820>✔️</emoji>Сообщение разослано по {count} из {len(chats)} чатам",
        reply_to_message_id=message.id)
