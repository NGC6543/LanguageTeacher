import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import quiz_words, different_types

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', 'svl3rf!30v3l')


async def main():
    """Run main functions."""
    logging.info('Enter to main Bot')
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_routers(quiz_words.router, different_types.router)
    print('Bot has started.')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler('log_main.log')
                  ],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())
