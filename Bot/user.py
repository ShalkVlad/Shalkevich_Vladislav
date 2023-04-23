from aiogram import types, Dispatcher

import db
from user_kb import But_User_Help, But_User_start, keyboard


async def command_start(message: types.Message):
    user_id = message.from_user.id
    if db.is_user_registered(user_id):
        await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=keyboard)
    else:
        await message.answer(f"Здравствуй, {message.from_user.full_name}!\n"
                             "Я бот для поиска новых людей по интересам! Я помогу найти тебе партнёра, что подобран "
                             "специально для тебя 😉", reply_markup=But_User_start)


async def command_help(message: types.Message):
    await message.answer("Выберете ваш вопрос", reply_markup=But_User_Help)


def reg(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(command_help, commands='help')
