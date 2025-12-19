from aiogram import Bot, Dispatcher
from asyncio import run
from config import BOT_TOKEN
import message, logging
from tortoise import Tortoise


dp = Dispatcher()
dp.include_router(message.router)

async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models.users', 'models.contents']}
    )
    await Tortoise.generate_schemas()

async def main():
    bot = Bot(token=BOT_TOKEN)
    
    await init_db()
    
    try:
        await dp.start_polling(bot)
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run(main())