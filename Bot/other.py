from aiogram import types, Dispatcher

import DB
from User_kb import start_keyboard, help_keyboard, main_keyboard


# Обработчик команды /start
async def command_start(message: types.Message):
    user_id = message.from_user.id
    if DB.is_user_registered(user_id):
        await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=main_keyboard)
    else:
        await message.answer(f"Здравствуй, {message.from_user.full_name}!\n"
                             "Я бот для поиска новых людей по интересам! Я помогу найти тебе партнёра, что подобран "
                             "специально для тебя 😉", reply_markup=start_keyboard)


# Обработчик команды /help
async def command_help(message: types.Message):
    await message.answer("Выберете ваш вопрос", reply_markup=help_keyboard)


# Регистрация обработчиков команд
def register(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(command_help, commands='help')
