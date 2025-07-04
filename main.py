import asyncio

from aiogram import Bot, Dispatcher

from app.bots.telegram.handlers import router
from app.config.settings import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
