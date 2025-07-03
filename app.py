# app.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from modules.chatbot.handlers import register_hello_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    register_hello_handlers(dp)

    logger.info("🚀 Bot iniciado")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
