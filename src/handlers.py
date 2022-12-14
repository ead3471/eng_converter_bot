from misc import dp, bot

from aiogram import types
from keyboards import main_keyboard, main_keyboard_buttons, temperature_units_keyboard, temperature_eu_buttons
import keyboards
from eng_unit_converter.measure import Measure
from aiogram.dispatcher import FSMContext
from state_machine import Convert


current_measure_class = None
current_measure_eu = None
current_measure_value = 0
current_measure: Measure = None


@dp.message_handler(commands=['start'])
async def start_converting(message: types.Message, state: FSMContext):

    await Convert.choosing_measure_type.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Выберете тип измерения",
                           reply_markup=main_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.endswith('measure'), state=Convert.choosing_measure_type)
async def process_measure_type(callback_query: types.CallbackQuery, state: FSMContext):
    pressed_button = keyboards.get_pressed_button(main_keyboard_buttons,
                                                  callback_query.data)
    selected_measure = pressed_button.measure_class

    global current_measure_class
    current_measure_class = selected_measure

    await bot.send_message(callback_query.from_user.id,
                           f'Выбрана {pressed_button.title}. Укажите значение')
    await Convert.next()


@dp.message_handler(state=Convert.set_value)
async def process_value(message: types.Message, state: FSMContext):
    global current_measure_value
    current_measure_value = float(message.text)
    await bot.send_message(message.chat.id, "Укажите единицы измерения", reply_markup=temperature_units_keyboard)
    await Convert.next()


@dp.callback_query_handler(lambda c: c.data and c.data.endswith('_temp_units'), state=Convert.choosing_eng_unit)
async def process_eng_units(callback_query: types.CallbackQuery, state: FSMContext):
    pressed_button = keyboards.get_pressed_button(temperature_eu_buttons,
                                                  callback_query.data)
    selected_units = pressed_button.measure_class

    global current_measure_eu, current_measure, current_measure_class
    current_measure_eu = selected_units

    current_measure = current_measure_class(
        current_measure_value, current_measure_eu)

    await bot.send_message(callback_query.from_user.id,
                           f'Текущее значение {current_measure}. Укажите единицы для перевода',
                           reply_markup=temperature_units_keyboard
                           )
    await Convert.next()


@dp.callback_query_handler(lambda c: c.data and c.data.endswith('_temp_units'), state=Convert.choosing_new_eng_unit)
async def process_new_eng_units(callback_query: types.CallbackQuery, state: FSMContext):
    pressed_button = keyboards.get_pressed_button(temperature_eu_buttons,
                                                  callback_query.data)

    global current_measure_eu, current_measure, current_measure_class
    new_measure_eu = pressed_button.measure_class

    converted_measure = current_measure.convert_to(new_measure_eu)

    await bot.send_message(callback_query.from_user.id,
                           f'Конвертированное значение {converted_measure}.',
                           )
    await Convert.next()
