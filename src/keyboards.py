from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from eng_unit_converter.measure import Measure, Temperature, MassFlow, ThermoResistor, AnalogSensorMeasure, Pressure
from dataclasses import dataclass
from typing import List


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


@dataclass
class MeasureButton:
    title: str
    callback: str
    measure_class: type


main_keyboard_buttons: List[List[MeasureButton]] = [
    [
        MeasureButton('Температурa', 'temp_measure', Temperature),
        MeasureButton('Давление', 'press_measure', Pressure),
        MeasureButton('Расход', 'flow_measure', MassFlow),],
    [
        MeasureButton('Терморезистор',
                      'thermo_resistor_measure', ThermoResistor),
        MeasureButton('Аналоговые измерения',
                      'analog_measure', AnalogSensorMeasure)
    ],

]


def create_keyboard(buttons_list: List[List[MeasureButton]], row_width: int = 3) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    for row in buttons_list:
        buttons_list = [
            InlineKeyboardButton(button.title, callback_data=button.callback)
            for button in row
        ]
        keyboard.add(*buttons_list)
    return keyboard


main_keyboard = create_keyboard(main_keyboard_buttons)


def get_pressed_button(keyboard_buttons: List[List[MeasureButton]], callback_data: str) -> MeasureButton:
    for row in keyboard_buttons:
        for button in row:
            if button.callback == callback_data:
                return button

    return Temperature


temperature_eu_buttons: List[List[MeasureButton]] = [
    [
        MeasureButton('C', 'celsius_temp_units', Temperature.SupportedUnits.C),
        MeasureButton('F', 'fahrenheit_temp_units',
                      Temperature.SupportedUnits.F),
        MeasureButton('K', 'kelvin_temp_units', Temperature.SupportedUnits.K),
    ]
]
temperature_units_keyboard = create_keyboard(temperature_eu_buttons)
