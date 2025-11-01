from pymax.types import FileRequest, PhotoAttach, FileAttach, VideoAttach
import requests
from pymax import MaxClient, Message
from aiogram.types import FSInputFile


async def prepare_attaches(
    client: MaxClient,
    message: Message,
) -> dict[tuple[FSInputFile, PhotoAttach | VideoAttach | FileAttach | None], str]:
    attaches = dict()
    path = "temp/"
    for attach in message.attaches:  # pyright: ignore
        attach_type = None
        url = None
        if isinstance(attach, PhotoAttach):
            url = attach.base_url
            path += f"{attach.photo_id}.webp"
            attach_type = PhotoAttach
        elif isinstance(attach, FileAttach):
            file: FileRequest = await client.get_file_by_id(
                message.chat_id,  # pyright: ignore
                message.id,
                attach.file_id,
            )
            url = file.url
            path += attach.name
            attach_type = FileAttach
        elif isinstance(attach, VideoAttach):
            video = await client.get_video_by_id(
                message.chat_id,  # pyright: ignore
                message.id,
                attach.video_id,
            )
            url = video.url  # pyright: ignore
            path += f"{attach.video_id}.webp"
            attach_type = VideoAttach

        attach_data = requests.get(url).content  # pyright: ignore
        with open(path, "wb") as f:
            f.write(attach_data)
        attaches[(FSInputFile(path), attach_type)] = path

    return attaches
