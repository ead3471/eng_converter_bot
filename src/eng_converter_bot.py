from aiogram import Bot, Dispatcher, executor, types
from eng_unit_converter.measure import Temperature, AnalogSensorMeasure
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Давление"),
         types.KeyboardButton(text="Температура"),
         types.KeyboardButton(text="Расход"),
         types.KeyboardButton(text="Термосопротивление"),
         types.KeyboardButton(text="Аналоговые датчики"),
         ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Что будем конвертировать?", reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
