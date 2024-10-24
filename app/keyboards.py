from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обычный прогноз погоды', callback_data='users')],
    [InlineKeyboardButton(text='Прогноз погоды для метеорологов', callback_data='professional')]

])
