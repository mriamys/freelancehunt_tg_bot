import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from bot.handlers import router
from database.storage import init_db
from services.monitor import start_monitoring
from services.cleaner import start_cleaner
from utils.logger import logger

async def main():
    # Инициализация БД
    await init_db()

    # Инициализация Бота
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Bot starting...")

    # Запуск фоновых задач
    monitor_task = asyncio.create_task(start_monitoring(bot))
    cleaner_task = asyncio.create_task(start_cleaner())

    # Запуск поллинга
    try:
        await dp.start_polling(bot)
    finally:
        monitor_task.cancel()
        cleaner_task.cancel()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
