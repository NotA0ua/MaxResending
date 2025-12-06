from json import loads
from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
GROUP_ID = getenv("GROUP_ID")
PHONE_NUMBER = getenv("PHONE_NUMBER")
CHATS: list[int] = list(map(int, loads(getenv("CHATS"))))  # pyright: ignore
