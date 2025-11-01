from dotenv import load_dotenv
from os import getenv
from json import loads

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
GROUP_ID = getenv("GROUP_ID")
PHONE_NUMBER = getenv("PHONE_NUMBER")
CHATS: list[int] = list(map(int, loads(getenv("CHATS"))))  # pyright: ignore
