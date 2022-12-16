from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from eng_unit_converter.measure import Measure, Temperature, MassFlow, ThermoResistor, AnalogSensorMeasure, Pressure
from dataclasses import dataclass
from typing import List, Dict


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


def create_keyboard(buttons_list: List[List[MeasureButton]],
                    row_width: int = 3) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    for row in buttons_list:
        buttons_list = [
            InlineKeyboardButton(button.title, callback_data=button.callback)
            for button in row
        ]
        keyboard.add(*buttons_list)
    keyboard.add(InlineKeyboardButton("В начало", callback_data="cancel"),
                 # InlineKeyboardButton("Шаг назад", callback_data="step_back")
                 )
    return keyboard


def create_eu_keyboard_for_measure(measure_type: type) -> InlineKeyboardMarkup:
    return create_keyboard(measure_units[measure_type])


def get_pressed_eu_button(measure_type: type,
                          callback_data: str) -> MeasureButton:
    return get_pressed_button(measure_units[measure_type], callback_data)


main_keyboard = create_keyboard(main_keyboard_buttons)


def get_pressed_button(keyboard_buttons: List[List[MeasureButton]],
                       callback_data: str) -> MeasureButton:
    for row in keyboard_buttons:
        for button in row:
            if button.callback == callback_data:
                return button
    return Temperature


measure_units: Dict[type, List[List[MeasureButton]]] = {
    Temperature: [[
        MeasureButton('C', 'celsius_temp_units', Temperature.SupportedUnits.C),
        MeasureButton('F', 'fahrenheit_temp_units',
                      Temperature.SupportedUnits.F),
        MeasureButton('K', 'kelvin_temp_units', Temperature.SupportedUnits.K),
    ]],
    Pressure: [
        [
            MeasureButton('атм', 'atm_press_units',
                          Pressure.SupportedUnits.atm),
            MeasureButton('Па', 'Pa_press_units',
                          Pressure.SupportedUnits.Pa),
            MeasureButton('кПа', 'kPa_press_units',
                          Pressure.SupportedUnits.kPa),
            MeasureButton('МПа', 'MPa_press_units',
                          Pressure.SupportedUnits.MPa),
            MeasureButton('кгс/см2', 'kgs_sm2_press_units',
                          Pressure.SupportedUnits.kgs_sm_2),
            MeasureButton('кгс/м2', 'kgs_m2_press_units',
                          Pressure.SupportedUnits.kgs_m_2),

        ],
        [
            MeasureButton('мм.вод.столба', 'mmh20_press_units',
                          Pressure.SupportedUnits.mm_h20),
            MeasureButton('м.вод.столба', 'mh20_press_units',
                          Pressure.SupportedUnits.m_h20),
            MeasureButton('мм.рт.ст.', 'bar_press_units',
                          Pressure.SupportedUnits.mm_hg),
            MeasureButton('бар', 'bar_press_units',
                          Pressure.SupportedUnits.bar),
        ]

    ]
}
