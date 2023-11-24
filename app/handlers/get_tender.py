import uuid
from datetime import datetime
import time
import validators
from aiogram import F, Router, Bot
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.function import tender_to_tender_name, choice_tender
from keyboard.reply_keyboard import create_tender_markup, start_markup, worked_tender_markup, get_tender_markup
from models.data import TenderName
from service.PostgresOrm import PostgresOrm
from settings import settings
from state_machine import CreateTender, DeleteTender, GetListTender

router = Router()


@router.message(StateFilter(None), F.text == 'Показать список тендеров')
async def create_tender(message: Message, state: FSMContext):
    await message.answer('Выберите список тендеров', reply_markup=get_tender_markup())
    await state.set_state(GetListTender.wait_list)


@router.message(StateFilter(GetListTender.wait_list))
async def create_tender(message: Message, state: FSMContext):
    if message.text == 'Список в работе':
        tenders = await PostgresOrm().get_tender_with_status(status='worked')
    elif message.text == "Список удаленных":
        tenders = await PostgresOrm().get_tender_with_status(status='deleted')
    elif message.text == "Список поданных":
        tenders = await PostgresOrm().get_tender_with_status(status='submitted')
    else:
        await state.set_state(None)
        await message.answer('Ошибка', reply_markup=start_markup())
        return
    tender_names = tender_to_tender_name(tenders)
    text = ''
    for tender in tender_names:
        text += tender.text
    await message.answer(text, reply_markup=start_markup())
    await state.set_state(None)
