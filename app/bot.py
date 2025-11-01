from io import BytesIO
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    BufferedInputFile,
    InputMediaPhoto,
    InputMediaVideo,
)
from pymax.types import FileAttach, PhotoAttach, VideoAttach
from app import BOT_TOKEN

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not provided in .env")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()


async def send_message(chat_id: int | str, text: str):
    await bot.send_message(chat_id=chat_id, text=text)


async def send_attaches(
    chat_id: int | str,
    text: str,
    attaches: list[tuple[BytesIO, PhotoAttach | VideoAttach | FileAttach | None]],
) -> None:
    media = list()
    for i, attach in enumerate(attaches):
        attach_type = attach[1]
        attach = attach[0]

        file = BufferedInputFile(attach.getvalue(), filename=attach.name)

        if attach_type == FileAttach:
            await bot.send_document(chat_id, file, caption=text)
            continue

        elif attach_type == PhotoAttach:
            if i == 0:
                media.append(InputMediaPhoto(media=file, caption=text))
            else:
                media.append(InputMediaPhoto(media=file))

        elif attach_type == VideoAttach:
            if i == 0:
                media.append(InputMediaVideo(media=file, caption=text))
            else:
                media.append(InputMediaVideo(media=file))
        else:
            return
    if media:
        await bot.send_media_group(chat_id=chat_id, media=media)
