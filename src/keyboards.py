from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from eng_unit_converter.measure import (Temperature,
                                        MassFlow,
                                        ThermoResistor,
                                        AnalogSensorMeasure,
                                        Pressure)
from dataclasses import dataclass
from typing import List, Dict

from misc import i18n

_ = i18n.lazy_gettext


@dataclass
class MeasureButton:
    title: str
    callback: str
    measure_class: type


commands_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
commands_menu_keyboard.add(
    KeyboardButton("/start"),
    KeyboardButton("/cstart"),
    KeyboardButton("/lang")
)


main_keyboard_buttons: List[List[MeasureButton]] = [
    [
        MeasureButton(_('Temperature'), 'temp_measure', Temperature),
        MeasureButton(_('Pressure'), 'press_measure', Pressure),
        MeasureButton(_('Mass Flow'), 'flow_measure', MassFlow),],
    [
        MeasureButton(_('Thermoresistor'),
                      'thermo_resistor_measure', ThermoResistor),
        MeasureButton(_('Analogue Measure'),
                      'analog_measure', AnalogSensorMeasure)
    ],
]


def create_keyboard(buttons_list: List[List[MeasureButton]],
                    row_width: int = 3,
                    add_cancel: bool = True
                    ) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    for row in buttons_list:
        buttons_list = [
            InlineKeyboardButton(button.title, callback_data=button.callback)
            for button in row
        ]
        keyboard.add(*buttons_list)
    if add_cancel:
        keyboard.add(InlineKeyboardButton(_("To the beginning"),
                                          callback_data="cancel")
                     )
    return keyboard


def create_eu_keyboard_for_measure(measure_type: type) -> InlineKeyboardMarkup:
    return create_keyboard(measure_units[measure_type])


def get_pressed_eu_button(measure_type: type,
                          callback_data: str) -> MeasureButton:
    return get_pressed_button(measure_units[measure_type], callback_data)


main_keyboard = create_keyboard(main_keyboard_buttons, add_cancel=False)


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
            MeasureButton(_('Pa'), 'Pa_press_units',
                          Pressure.SupportedUnits.Pa),
            MeasureButton(_('kPa'), 'kPa_press_units',
                          Pressure.SupportedUnits.kPa),
            MeasureButton(_('MPa'), 'MPa_press_units',
                          Pressure.SupportedUnits.MPa),
            MeasureButton(_('kgf/sm2'), 'kgs_sm2_press_units',
                          Pressure.SupportedUnits.kgs_sm_2),
            MeasureButton(_('kgf/m2'), 'kgs_m2_press_units',
                          Pressure.SupportedUnits.kgs_m_2),

        ],
        [
            MeasureButton(_('mm.water.column'), 'mmh20_press_units',
                          Pressure.SupportedUnits.mm_h20),
            MeasureButton(_('m.water.column'), 'mh20_press_units',
                          Pressure.SupportedUnits.m_h20),
            MeasureButton(_('mm.hg.column'), 'bar_press_units',
                          Pressure.SupportedUnits.mm_hg),
            MeasureButton(_('bar'), 'bar_press_units',
                          Pressure.SupportedUnits.bar),
        ],
        [
            MeasureButton(_('atm physical'), 'atm_ph_press_units',
                          Pressure.SupportedUnits.atm_ph),
            MeasureButton(_('atm technical'), 'atm_tech_press_units',
                          Pressure.SupportedUnits.atm_t),
        ]

    ],
    ThermoResistor: [
        [
            MeasureButton('C', 'celsius_tr_units',
                          ThermoResistor.SupportedUnits.C),
            MeasureButton('F', 'fahrenheit_tr_units',
                          ThermoResistor.SupportedUnits.F),
            MeasureButton('K', 'kelvin_tr_units',
                          ThermoResistor.SupportedUnits.K),
        ],
        [
            MeasureButton('Pt100', 'Pt100_tr_units',
                          ThermoResistor.SupportedUnits.Pt100_Ohm),
            MeasureButton('100П', '100P_tr_units',
                          ThermoResistor.SupportedUnits.P100_Ohm),
            MeasureButton('Ni100', 'Ni100_tr_units',
                          ThermoResistor.SupportedUnits.Ni100_Ohm),
            MeasureButton('Cu100', 'Cu100_tr_units',
                          ThermoResistor.SupportedUnits.Cu100_Ohm)
        ]
    ],
    MassFlow: [
        [
            MeasureButton(_('kg/h'), 'mass_rhg_units',
                          MassFlow.SupportedUnits.kg_h),
            MeasureButton(_('kg/d'), 'mass_kgd_units',
                          MassFlow.SupportedUnits.kg_d),
            MeasureButton(_('kg/s'), 'mass_kgs_units',
                          MassFlow.SupportedUnits.kg_s),
            MeasureButton(_('t/h'), 'mass_th_units',
                          MassFlow.SupportedUnits.t_h),
            MeasureButton(_('t/s'), 'mass_ts_units',
                          MassFlow.SupportedUnits.t_s),
        ]
    ],
    AnalogSensorMeasure: [

        [
            MeasureButton('%', 'percent_units',
                          AnalogSensorMeasure.SupportedUnits.persent),
            MeasureButton(_('4-20 mA'), '4_20_units',
                          AnalogSensorMeasure.SupportedUnits.mA_4_20),
            MeasureButton(_('0-20 мА'), '0_20_units',
                          AnalogSensorMeasure.SupportedUnits.mA_0_20),
        ],

        [
            MeasureButton(_('1-5 V'), '1_5_units',
                          AnalogSensorMeasure.SupportedUnits.V_1_5),
            MeasureButton(_('Physical units'), 'Physical_units',
                          AnalogSensorMeasure.SupportedUnits.MEASURE),
        ]


    ]

}
