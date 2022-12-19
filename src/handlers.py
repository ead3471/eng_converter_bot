from misc import dp, bot

from aiogram import types
from keyboards import (main_keyboard,
                       main_keyboard_buttons,
                       create_eu_keyboard_for_measure)
import keyboards
from aiogram.dispatcher import FSMContext
from state_machine import Convert
from eng_unit_converter.measure import Measure
from aiogram.utils.markdown import text, hbold


@dp.message_handler(commands=['start'])
async def start_converting(message: types.Message, state: FSMContext):
    await Convert.choosing_measure_type.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text=text(
                               hbold(
                                   f"Hello, {message.from_user.username}!\n"),
                               "I'm a engineering units converter bot.\n",
                               "Choose type of measure please.s"),
                           reply_markup=main_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data == 'cancel',
                           state='*')
async def process_cancel(callback_query: types.CallbackQuery,
                         state: FSMContext):
    await Convert.choosing_measure_type.set()
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Choose measure type.",
                           reply_markup=main_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.endswith('measure'),
                           state=Convert.choosing_measure_type)
async def process_measure_type_choosen(callback_query: types.CallbackQuery,
                                       state: FSMContext):
    pressed_button = keyboards.get_pressed_button(main_keyboard_buttons,
                                                  callback_query.data)
    await state.update_data(measure_class=pressed_button.measure_class)

    await bot.send_message(
        callback_query.from_user.id,
        text=text(
            hbold(str(pressed_button.title)),
            'is selected.'
            '\nSet value please.'))
    await Convert.next()


@dp.message_handler(state=Convert.set_value)
async def process_value(message: types.Message, state: FSMContext):
    current_measure_value = float(message.text)
    measure_class = (await state.get_data())['measure_class']
    await state.update_data(value=float(current_measure_value))
    await bot.send_message(message.chat.id, "Select measure units please.",
                           reply_markup=create_eu_keyboard_for_measure(
                               measure_class))
    await Convert.next()


@ dp.callback_query_handler(lambda c: c.data and c.data.endswith('_units'),
                            state=Convert.choosing_eng_unit)
async def process_eng_units_choosen(callback_query: types.CallbackQuery,
                                    state: FSMContext):
    user_data = await state.get_data()
    measure_class = user_data['measure_class']
    pressed_button = keyboards.get_pressed_eu_button(measure_class,
                                                     callback_query.data)
    selected_units = pressed_button.measure_class
    await state.update_data(eu=selected_units)

    current_measure: Measure = user_data['measure_class'](
        user_data['value'], selected_units)

    await state.update_data(measure=current_measure)

    await bot.send_message(callback_query.from_user.id,
                           text=text(
                               'Current value is\n',
                               hbold(current_measure),
                               '\nSelect new measure units please.',
                           ),
                           reply_markup=create_eu_keyboard_for_measure(
                               measure_class)
                           )
    await Convert.next()


@dp.callback_query_handler(lambda c: c.data and c.data.endswith('_units'),
                           state=Convert.choosing_new_eng_unit)
async def process_convertion_units_choosen(callback_query: types.CallbackQuery,
                                           state: FSMContext):

    user_data = await state.get_data()
    measure_class = user_data['measure_class']
    pressed_button = keyboards.get_pressed_eu_button(measure_class,
                                                     callback_query.data)

    new_measure_eu = pressed_button.measure_class

    current_measure: Measure = user_data['measure']
    converted_measure: Measure = current_measure.convert_to(
        new_measure_eu)

    await bot.send_message(callback_query.from_user.id,
                           text=str(converted_measure)

                           )
