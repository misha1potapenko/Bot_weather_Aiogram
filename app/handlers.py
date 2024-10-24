from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup,State


router = Router()


class Town(StatesGroup):
    name_town = State

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, я бот прогноза погоды. Пожалуйста, выбери кнопочку ниже, какой прогноз тебе нужен.',
                         reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Напиши еще раз название города, если не работает, я сломался((((")


@router.message(F.text == 'Как дела')
async def how_are_you(message: Message):
    await message.answer("Ok")


@router.callback_query(F.data == 'users')
async def for_users(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Напишите название города')

@router.callback_query(F.data == 'professional')
async def for_professional(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Напишите название города')