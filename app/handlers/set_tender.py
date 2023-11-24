import uuid
from datetime import datetime
import time
import validators
from aiogram import F, Router, Bot
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.function import tender_to_tender_name, choice_tender
from keyboard.reply_keyboard import create_tender_markup, start_markup, worked_tender_markup
from models.data import TenderName
from service.PostgresOrm import PostgresOrm
from settings import settings
from state_machine import CreateTender, DeleteTender, SetTender

router = Router()


@router.message(StateFilter(None), Command("/подать_заявку"), )
async def create_tender(message: Message, state: FSMContext):
    await choice_tender(message, state, 'worked')
    await state.set_state(SetTender.wait_reg_num)


@router.message(StateFilter(None), F.text == 'Подать заявку')
async def create_tender(message: Message, state: FSMContext):
    await choice_tender(message, state, 'worked')
    await state.set_state(SetTender.wait_reg_num)


@router.message(StateFilter(SetTender.wait_reg_num))
async def create_tender(message: Message, state: FSMContext):
    await choice_tender(message, state)
    data = await state.get_data()
    tender_names: list[TenderName] = data['tender_names']
    tender_id: uuid.UUID | None = None
    texts = [tender.text for tender in tender_names]
    urls = [tender.tender.url for tender in tender_names]
    regs_num = [tender.tender.registration_number for tender in tender_names]
    tr = texts + urls + regs_num
    if message.text in tr:
        for tender in tender_names:
            if (message.text == tender.text or
                    message.text == tender.tender.registration_number or
                    message.text == tender.tender.url):
                tender_id = tender.tender.id
        if tender_id:
            await PostgresOrm().update_tender(tender_id, status='submitted')
            await message.answer('Статус изменен', reply_markup=start_markup())
    else:
        await message.answer('Тендер не найден', reply_markup=start_markup())
