"""Utilities to create and run the Telegram bot."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from modules.chatbot import router as chatbot_router
from modules.guess_flag import router as flag_router
from modules.guess_position import router as guess_router

logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    """Instantiate and return a configured :class:`Bot`."""
    return Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    """Create dispatcher and register all routers."""
    dp = Dispatcher()
    dp.include_router(chatbot_router)
    dp.include_router(guess_router)
    dp.include_router(flag_router)
    return dp


async def run_polling() -> None:
    """Start polling using created bot and dispatcher."""
    bot = create_bot()
    dp = create_dispatcher()
    logger.info("🤖 Bot iniciado y listo...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_polling())

