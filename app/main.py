from __future__ import annotations
import asyncio
import os
from services.storage import S3Storage
from bot.bot import bot, dp
import aiohttp


async def start_server():
    from uvicorn import Config, Server
    config = Config("app:app", port=8001, host="127.0.0.1", reload=True)
    server = Server(config)
    await server.serve()

async def start_bot():
        await dp.start_polling(bot)

async def main():
    os.environ.clear()
    # Запуск бота
    task1 = asyncio.create_task(start_bot())
    task2 = asyncio.create_task(start_server())
    await asyncio.gather(task1, task2)
    

if __name__ == "__main__":
    storage = S3Storage()
    data = storage.get("photo_2025-06-01_01-24-55.jpg")
    print(data)
    asyncio.run(main())