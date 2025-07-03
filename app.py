"""Entry point to run the Telegram bot."""

import asyncio

from core.bot import run_polling


if __name__ == "__main__":
    asyncio.run(run_polling())
