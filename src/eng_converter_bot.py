
from misc import dp

from aiogram.utils import executor
import handlers

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
