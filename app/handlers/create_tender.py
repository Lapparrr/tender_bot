from datetime import datetime
import time
import validators
from aiogram import F, Router, Bot
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboard.reply_keyboard import create_tender_markup, start_markup
from service.PostgresOrm import PostgresOrm
from settings import settings
from state_machine import CreateTender

router = Router()


@router.message(StateFilter(None), Command("/добавить_тендер"), )
async def create_tender(message: Message, state: FSMContext):
    await message.answer("Выберете режим на кнопках", reply_markup=create_tender_markup())
    await state.set_state(CreateTender.wait_mode)


@router.message(StateFilter(None), F.text == 'Добавить тендер')
async def create_tender(message: Message, state: FSMContext):
    await message.answer("Выберете режим на кнопках", reply_markup=create_tender_markup())
    await state.set_state(CreateTender.wait_mode)


@router.message(StateFilter(CreateTender.wait_mode))
async def create_tender(message: Message, state: FSMContext):
    if message.text == "Создать в автоматическом режиме":
        await state.set_state(CreateTender.wait_url)
        await message.answer('Отправьте ссылку на тендер')
        pass
    elif message.text == 'Создать в ручном режиме':
        await state.set_state(CreateTender.manual_name)
        await message.answer('Отправьте название тендера')
    else:
        await state.set_state(None)
        await message.answer('Такого режима нет', reply_markup=start_markup())


@router.message(StateFilter(CreateTender.wait_url))
async def create_tender(message: Message, state: FSMContext):
    await message.answer('Данный функционал пока не реализован')
    # TODO реализовать парсер


@router.message(StateFilter(CreateTender.manual_name))
async def create_tender(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Отправьте ссылку на тендер')
    await state.set_state(CreateTender.manual_irl)


@router.message(StateFilter(CreateTender.manual_irl))
async def create_tender(message: Message, state: FSMContext):
    if not validators.url(message.text):
        await message.answer('Неправильный формат ссылки')
        return
    await state.update_data(url=message.text)
    await message.answer('Отправьте дату окончания на тендера в формате'
                         'день.месяц.год часы:минуты\n'
                         'Пример: 30.11.2023 08:00')
    await state.set_state(CreateTender.manual_date)


@router.message(StateFilter(CreateTender.manual_date))
async def create_tender(message: Message, state: FSMContext):
    try:
        datetime_obj = datetime.strptime(message.text+':00', '%d.%m.%Y %H:%M:%S')
    except Exception as e:
        await message.answer("Неправильный формат даты")
        raise e
    await state.update_data(datetime=datetime_obj)
    await message.answer('Отправьте регистрационный номер')
    await state.set_state(CreateTender.manual_reg_num)


@router.message(StateFilter(CreateTender.manual_reg_num))
async def create_tender(message: Message, state: FSMContext):
    data = await state.get_data()
    url = data['url']
    date_time = data['datetime']
    name = data['name']
    reg_num = message.text
    try:
        await PostgresOrm().create_tender(name=name, reg_num=reg_num, datetime=date_time, url=url)
        await message.answer('Сохранено')
    except Exception as e:
        await message.answer('Ошибка при сохранении')
        raise e
