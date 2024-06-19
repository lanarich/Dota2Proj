import asyncio
import logging

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
import os
from utils.commands import set_commands
from handlers import predict_items, user_mark, statistics, start, pick_fun, fastapi_handlers, als_handler, Sas_hendler


load_dotenv()

token = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()


dp.include_routers(
    predict_items.router,
    user_mark.router_mark,
    statistics.router_stat,
    start.router_start,
    pick_fun.router_pick,
    fastapi_handlers.router_stats,
    als_handler.router_als,
    Sas_hendler.router_sas)


async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
