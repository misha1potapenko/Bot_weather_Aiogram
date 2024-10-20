import asyncio

import aiogram
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, я бот прогноза погоды. Напиши мне название города, а я скину тебе прогноз.')


@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Напиши еще раз название города, если не работает, я сломался((((")


@dp.message(F.text == 'Как дела')
async def how_are_you(message: Message):
    await message.answer("Ok")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
