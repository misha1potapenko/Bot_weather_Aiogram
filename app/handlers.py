from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, я бот прогноза погоды. Напиши мне название города, а я скину тебе прогноз.')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Напиши еще раз название города, если не работает, я сломался((((")


@router.message(F.text == 'Как дела')
async def how_are_you(message: Message):
    await message.answer("Ok")