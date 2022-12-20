from misc import dp, bot

from aiogram import types
from keyboards import (main_keyboard,
                       main_keyboard_buttons,
                       create_eu_keyboard_for_measure)
import keyboards
from aiogram.dispatcher import FSMContext
from state_machine import Convert
from eng_unit_converter.measure import Measure, AnalogSensorMeasure
from aiogram.utils.markdown import text, hbold


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


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


@dp.message_handler(lambda message: is_float(message.text),
                    state=Convert.set_measure_value)
async def process_measure_value(message: types.Message, state: FSMContext):
    current_measure_value = float(message.text)
    measure_class = (await state.get_data())['measure_class']
    await state.update_data(value=float(current_measure_value))
    await bot.send_message(message.chat.id, "Select measure units please.",
                           reply_markup=create_eu_keyboard_for_measure(
                               measure_class))
    await Convert.next()


@dp.message_handler(lambda message: not is_float(message.text),
                    state=Convert.set_measure_value)
async def process_bad_measure_value(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "The value must be a number!")


@dp.message_handler(lambda message: not is_float(message.text),
                    state=Convert.choosing_analog_scale_low)
async def process_bad_low_scale(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "The value must be a number!")


@dp.message_handler(lambda message: not is_float(message.text),
                    state=Convert.choosing_analog_scale_hi)
async def process_bad_hi_scale(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "The value must be a number!")


@dp.callback_query_handler(lambda c: c.data and c.data.endswith('_units'),
                           state=Convert.choosing_measure_eng_unit)
async def process_measure_eng_units_choosen(
        callback_query: types.CallbackQuery,
        state: FSMContext):
    user_data = await state.get_data()
    measure_class = user_data['measure_class']
    pressed_button = keyboards.get_pressed_eu_button(measure_class,
                                                     callback_query.data)
    selected_units = pressed_button.measure_class
    await state.update_data(measure_eu=selected_units)

    selected_measure_type: Measure = user_data['measure_class']
    if selected_measure_type is AnalogSensorMeasure:
        await bot.send_message(callback_query.from_user.id,
                               text="Set physical measure scale low")
        await Convert.next()
    else:
        current_measure: Measure = selected_measure_type(
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
        await Convert.choosing_new_eng_unit.set()


@dp.message_handler(lambda message: is_float(message.text),
                    state=Convert.choosing_analog_scale_low)
async def process_physical_measure_scale_low(message: types.Message,
                                             state: FSMContext):
    physical_measure_scale_low = float(message.text)

    await state.update_data(
        physical_measure_scale_low=float(physical_measure_scale_low))
    await bot.send_message(message.chat.id, "Set physical value scale hi")
    await Convert.next()


@dp.message_handler(lambda message: is_float(message.text),
                    state=Convert.choosing_analog_scale_hi)
async def process_physical_measure_scale_hi(message: types.Message,
                                            state: FSMContext):
    physical_measure_scale_hi = float(message.text)

    await state.update_data(
        physical_measure_scale_hi=float(physical_measure_scale_hi))
    await bot.send_message(message.chat.id, "Set physical value eu")
    await Convert.next()


@dp.message_handler(state=Convert.choosing_analog_eu)
async def process_physical_measure_eu(message: types.Message,
                                      state: FSMContext):
    physical_measure_eu = message.text

    await state.update_data(
        physical_measure_eu=physical_measure_eu)

    user_data = await state.get_data()
    selected_measure_class = user_data['measure_class']
    selected_units = user_data['measure_eu']
    value = user_data['value']
    ph_scale_low = user_data['physical_measure_scale_low']
    ph_scale_hi = user_data['physical_measure_scale_hi']

    current_measure: Measure = AnalogSensorMeasure(
        value, selected_units, ph_scale_low, ph_scale_hi, physical_measure_eu)

    await state.update_data(measure=current_measure)

    await bot.send_message(message.from_user.id,
                           text=text(
                               'Current value is\n',
                               hbold(current_measure),
                               '\nSelect new measure units please.',
                           ),
                           reply_markup=create_eu_keyboard_for_measure(
                               selected_measure_class)
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
                           text=text(hbold(str(current_measure)),
                                     '\n is equal to\n',
                                     hbold(str(converted_measure)))
                           )
