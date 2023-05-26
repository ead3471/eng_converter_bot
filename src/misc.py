from dotenv import load_dotenv
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from middlewares import I18nMiddleware
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL") or logging.INFO


APP_DIR: Path = Path(__file__).parent.parent
LOCALES_DIR = APP_DIR / "locales"
LOGS_DIR = APP_DIR / "logs"
logger = logging.getLogger(__name__)


def init_logger(logging_level=logging.DEBUG):
    os.makedirs(LOGS_DIR, exist_ok=True)
    handler = TimedRotatingFileHandler(
        filename=LOGS_DIR / "handler_log",
        when="D",
        interval=1,
        backupCount=30,
        encoding="utf-8",
        delay=False,
    )
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    handler.suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")

    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging_level)
    logger.info(f"Log inited. Logging level={logging_level}")


storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
i18n = I18nMiddleware("bot", LOCALES_DIR, default="ru")


def setup():
    init_logger(logging_level=LOG_LEVEL)
    dp.middleware.setup(i18n)
