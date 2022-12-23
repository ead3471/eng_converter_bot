from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import types
from misc import dp, bot
from keyboards import main_keyboard


class Convert(StatesGroup):
    choosing_measure_type = State()
    set_measure_value = State()
    choosing_measure_eng_unit = State()

    choosing_analog_scale_low = State()
    choosing_analog_scale_hi = State()
    choosing_analog_eu = State()

    choosing_new_eng_unit = State()
