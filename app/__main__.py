import asyncio

from app.bot import dp, bot
from app.max import client


async def main():
    task_bot = asyncio.create_task(dp.start_polling(bot))
    task_max = asyncio.create_task(client.start())
    await asyncio.gather(task_bot, task_max)


if __name__ == "__main__":
    asyncio.run(main())
