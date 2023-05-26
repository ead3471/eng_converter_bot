from misc import dp, setup

from aiogram.utils import executor
import handlers

if __name__ == "__main__":
    setup()
    executor.start_polling(dp, skip_updates=True)
