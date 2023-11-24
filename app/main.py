import asyncio

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from handlers import start, create_tender, delete_tender, get_tender, set_tender
from db.postgres import PostgresConnectAsync

from settings import settings


async def main():
    await PostgresConnectAsync().create_database()
    bot = Bot(settings.telegram_token, parse_mode=ParseMode.HTML, )
    dp = Dispatcher()
    dp.include_routers(
        start.router,
        create_tender.router,
        delete_tender.router,
        get_tender.router,
        set_tender.router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    pass
