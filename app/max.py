import asyncio

from pymax import MaxClient, Message, MessageStatus

from app import CHATS, GROUP_ID, PHONE_NUMBER
from app.bot import send_attaches, send_message
from app.utils import prepare_attaches

if not PHONE_NUMBER:
    raise ValueError("PHONE_NUMBER is not provided in .env")

if not GROUP_ID:
    raise ValueError("GROUP_ID is not provided in .env")

if not CHATS:
    raise ValueError("CHATS is not provided in .env")


client = MaxClient(phone=PHONE_NUMBER, work_dir="cache")
logger = client.logger


@client.on_message()
async def handle_message(message: Message) -> None:
    # Проверка на нахождение в чате
    if message.chat_id not in CHATS:
        return

    if not message.sender:
        return

    user = await client.get_user(message.sender)

    if not user:
        return

    message_text = message.text
    if not message.text:
        if message.link and message.link.message.text:
            message_text = message.link.message.text
        else:
            message_text = "Пустое сообщение"
    text = f"```{user.names[0].name if user.names else 'Неизвестный пользователь'}\n{message_text}```"

    if message.status == MessageStatus.REMOVED:
        return
    if message.status == MessageStatus.EDITED:
        text = "✏️ Сообщение было изменено\n" + text

    if message.attaches:
        attaches = await prepare_attaches(client, message)
        await send_attaches(chat_id=GROUP_ID, text=text, attaches=attaches)
    else:
        await send_message(chat_id=GROUP_ID, text=text)


@client.on_start
async def handle_start() -> None:
    logger.info("Клиент запущен")
    for chat in client.chats:
        logger.info(f"{chat.title}: {chat.id}")


async def main() -> None:
    await client.start()
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
