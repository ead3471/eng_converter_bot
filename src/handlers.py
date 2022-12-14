from misc import dp, bot

from aiogram import types
from keyboards import main_keyboard
import keyboards
from eng_unit_converter.measure import Measure


current_measure_class = None
current_measure_eu = None
current_measure_value = 0


@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Выберете тип измерения", reply_markup=main_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.endswith('measure'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    pressed_button = keyboards.get_measure_from_measure_keyboard_callback_data(
        callback_query.data)
    selected_measure = pressed_button.callback

    global current_measure_class
    current_measure_class = selected_measure

    await bot.send_message(callback_query.from_user.id, f'Выбрана {pressed_button.title}. Укажите значение')


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_value(callback_query: types.CallbackQuery):
    


    global current_measure_class
    current_measure_class=selected_measure

    await bot.send_message(callback_query.from_user.id, f'Выбрана {pressed_button.title}. Укажите значение')
