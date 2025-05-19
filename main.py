import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import register_handlers

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    register_handlers(dp, bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())