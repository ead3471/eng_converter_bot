from dotenv import load_dotenv
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from middlewares import I18nMiddleware
from pathlib import Path
load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")


app_dir: Path = Path(__file__).parent.parent
locales_dir = app_dir / "locales"

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
i18n = I18nMiddleware("bot", locales_dir, default="ru")
dp.middleware.setup(i18n)
