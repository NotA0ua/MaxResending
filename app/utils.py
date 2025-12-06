from io import BytesIO

import aiohttp
from pymax import AttachType, MaxClient, Message
from pymax.types import FileAttach, PhotoAttach, VideoAttach


async def prepare_attaches(
    client: MaxClient,
    message: Message,
) -> list[tuple[BytesIO, PhotoAttach | VideoAttach | FileAttach | None]]:
    attaches = []

    if not message.attaches:
        return attaches

    for attach in message.attaches:
        if not message.chat_id:
            continue

        attach_type = None
        url = None
        if attach.type == AttachType.PHOTO:
            url = attach.base_url
            attach_type = PhotoAttach
        elif attach.type == AttachType.FILE:
            file = await client.get_file_by_id(
                message.chat_id,
                message.id,
                attach.file_id,
            )
            if not file:
                continue
            url = file.url
            attach_type = FileAttach
        elif attach.type == AttachType.VIDEO:
            video = await client.get_video_by_id(
                message.chat_id,
                message.id,
                attach.video_id,
            )
            url = video.url
            attach_type = VideoAttach

        if not url or not attach_type:
            continue

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    attach_bytes = BytesIO(await response.read())
                    attach_bytes.name = response.headers.get("X-File-Name")
                    attaches.append((attach_bytes, attach_type))

            except aiohttp.ClientError as e:
                print(f"Ошибка при загрузке изображения: {e}")
            except Exception as e:
                print(f"Ошибка при отправке фото: {e}")

    return attaches
