from io import BytesIO
from pymax.types import FileRequest, PhotoAttach, FileAttach, VideoAttach
from pymax import MaxClient, Message
from aiogram.types import FSInputFile
import aiohttp


async def prepare_attaches(
    client: MaxClient,
    message: Message,
) -> list[tuple[BytesIO, PhotoAttach | VideoAttach | FileAttach | None]]:
    attaches = list()
    for attach in message.attaches:  # pyright: ignore
        attach_type = None
        url = None
        if isinstance(attach, PhotoAttach):
            url = attach.base_url
            attach_type = PhotoAttach
        elif isinstance(attach, FileAttach):
            file: FileRequest = await client.get_file_by_id(
                message.chat_id,  # pyright: ignore
                message.id,
                attach.file_id,
            )
            url = file.url
            attach_type = FileAttach
        elif isinstance(attach, VideoAttach):
            video = await client.get_video_by_id(
                message.chat_id,  # pyright: ignore
                message.id,
                attach.video_id,
            )
            url = video.url  # pyright: ignore
            attach_type = VideoAttach

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:  # pyright: ignore
                    response.raise_for_status()
                    photo_bytes = BytesIO(await response.read())
                    photo_bytes.name = response.headers.get("X-File-Name")
                    attaches.append((photo_bytes, attach_type))

            except aiohttp.ClientError as e:
                print(f"Ошибка при загрузке изображения: {e}")
            except Exception as e:
                print(f"Ошибка при отправке фото: {e}")

    return attaches
