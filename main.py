"""
Quiz Bot - Main Entry Point
Telegram bot for creating and taking IT quizzes with AI support
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_BOT_TOKEN
from bot.handlers import user, admin
from services import init_db


async def main():
    """Main function to start the bot"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize database
    init_db()
    logging.info("Database initialized")

    # Initialize bot and dispatcher
    assert TELEGRAM_BOT_TOKEN is not None, "TELEGRAM_BOT_TOKEN is not set"
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # Start polling
    logging.info("Starting Quiz Bot...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
