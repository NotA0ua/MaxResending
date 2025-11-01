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

    user = await client.get_user(message.sender)  # pyright: ignore

    message_text = message.text
    if not message.text:
        message_text = "Пустое сообщение"
    text = f"```{user.names[0].name}\n{message_text}```"  # pyright: ignore

    if message.status == MessageStatus.REMOVED:
        return
    elif message.status == MessageStatus.EDITED:
        text = "✏️ Сообщение было изменено\n" + text

    if message.attaches:
        attaches = await prepare_attaches(client, message)
        await send_attaches(chat_id=GROUP_ID, text=text, attaches=attaches)  # pyright: ignore
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
