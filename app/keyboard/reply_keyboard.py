from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from models.data import TenderName



def get_tender_markup():
    builder = ReplyKeyboardBuilder()
    button = ['Список в работе', "Список удаленных", "Список поданных"]
    for name in button:
        builder.add(KeyboardButton(text=name))
    builder.add(KeyboardButton(text="Отмена"))
    builder.adjust(1)
    return builder.as_markup(is_persistent=True)


def worked_tender_markup(tenders: list[TenderName]):
    builder = ReplyKeyboardBuilder()
    for tender in tenders:
        builder.add(KeyboardButton(text=tender.tender.registration_number))
    builder.add(KeyboardButton(text="Отмена"))
    builder.adjust(1)
    return builder.as_markup(is_persistent=True)


def start_markup():
    builder = ReplyKeyboardBuilder()
    button = ['Добавить тендер', "Подать заявку", "Удалить тендер", "Показать список тендеров"]
    for name in button:
        builder.add(KeyboardButton(text=name))
    builder.adjust(1)
    return builder.as_markup(is_persistent=True)


def create_tender_markup():
    builder = ReplyKeyboardBuilder()
    button = ['Создать в автоматическом режиме', "Создать в ручном режиме", "Отмена"]
    for name in button:
        builder.add(KeyboardButton(text=name))
    builder.adjust(1)
    return builder.as_markup(is_persistent=True)
