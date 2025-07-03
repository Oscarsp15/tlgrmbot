# app.py

import asyncio
from aiogram import Bot, Dispatcher, DefaultBotProperties
from config import BOT_TOKEN
from modules.chatbot.handlers import register_hello_handlers

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Registrar handlers
    register_hello_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
