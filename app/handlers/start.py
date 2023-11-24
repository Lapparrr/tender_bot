from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext, Any
from aiogram.types import Message

from keyboard.reply_keyboard import start_markup

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message,
                                state: FSMContext) -> None:
    await state.set_state(None)
    await message.answer(f"Привет, {message.from_user.full_name}!\n Для отмены любой команды пиши в чат <b>Отмена<b>",
                         parse_mode=None, reply_markup=start_markup()
                         )


@router.message(F.text == 'Отмена')
async def command_start_handler(message: Message,
                                state: FSMContext) -> None:
    await state.set_state(None)
    await message.answer(f"Возвращаю в главное меню!\n",
                         parse_mode=None, reply_markup=start_markup()
                         )
