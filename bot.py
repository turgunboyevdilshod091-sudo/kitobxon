import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from database.databse import Database
from handlers.start import router as start_router
from handlers.book import router as book_router
from handlers.admin.admin import router as admin_router
from handlers.addbook.addbook import addbook_router as add_router
from handlers.save import router as save_router
from handlers.search import router as search_router
from handlers.foydali import router as foydali_maslahatlar_router
from handlers.views import router as views_router
from handlers.settings import router as settings_router
from handlers.stats import router as stats_router
from handlers.random import router as random_router
from handlers.inline_mode import router as inline_mode_router

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    db = Database()
    await db.connect()

    dp["db"] = db

    dp.include_router(search_router)
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(add_router)
    dp.include_router(save_router)
    dp.include_router(book_router)
    dp.include_router(views_router)
    dp.include_router(random_router)
    dp.include_router(inline_mode_router)
    dp.include_router(settings_router)
    dp.include_router(stats_router)
    dp.include_router(foydali_maslahatlar_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
