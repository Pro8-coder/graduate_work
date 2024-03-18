import asyncio
import logging
import sqlite_db
from core.handlers import basic, admine, cart, pay
from aiogram import Bot, Dispatcher
from config import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession, BasicAuth, \
    ClientSession, TCPConnector


async def main():
    """Запуск бота и регистрация хэндлеров/роутеров"""
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_routers(basic.router)
    dp.include_routers(cart.router)
    dp.include_routers(pay.router)
    dp.include_routers(admine.router)

    try:
        await dp.start_polling(bot, storage=storage,
                               on_startup=sqlite_db.sql_start())
    except asyncio.exceptions.CancelledError:
        await bot.session.close()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
