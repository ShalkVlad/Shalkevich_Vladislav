from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from DataBase import DB, Profil_vere
from Language.Language import load_language_texts, get_user_language, get_user_texts, Language
from User_Keybord.User_kb import start, main, helps


def cancels(func):
    async def cancel_Reg(message: types.Message, state: FSMContext, *args, **kwargs):
        # Проверка на отмену регистрации
        texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
        user_id = message.from_user.id
        user = DB.get_user(user_id)
        preferences = user.photo
        if message.text.strip() == texts["cancelS"]:
            if not user.photo:
                await state.finish()
                await message.answer(texts["cancel_message"], reply_markup=start(texts))
            else:
                await state.finish()
                await message.answer(texts["cancel_message"], reply_markup=main(texts))
        elif message.text.strip() == texts["Cancel"]:
            await state.finish()
            await message.answer(texts["update_cancelled"], reply_markup=main(texts))
        else:
            # Вызываем обработчик сообщения и передаем `texts` как аргумент
            await func(message, state, texts, preferences, user_id, *args, **kwargs)

            # Здесь можно выполнить какие-либо действия после выполнения функции

    return cancel_Reg


def cancel(func):
    async def cancel_registration(message: types.Message, state: FSMContext, *args, **kwargs):
        # Проверка на отмену регистрации
        texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
        user_id = message.from_user.id
        user = DB.get_user(user_id)
        preferences = Profil_vere.get_user_preferences(user_id)
        if message.text.strip() == texts["cancelS"]:
            if not user.photo:
                await state.finish()
                await message.answer(texts["cancel_message"], reply_markup=start(texts))
            else:
                await state.finish()
                await message.answer(texts["cancel_message"], reply_markup=main(texts))
        elif message.text.strip() == texts["Cancel"]:
            await state.finish()
            await message.answer(texts["update_cancelled"], reply_markup=main(texts))
        else:
            # Вызываем обработчик сообщения и передаем `texts` как аргумент
            await func(message, state, texts, preferences, user_id, *args, **kwargs)

            # Здесь можно выполнить какие-либо действия после выполнения функции

    return cancel_registration


# Обработчик команды /start
async def command_start(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    user_id = message.from_user.id
    user = DB.get_user(user_id)
    if not DB.is_user_registered(message.from_user.id):
        DB.create_profile(user_id, "", 0, "", "", "",
                          "", "", "", "Русский")
        await message.answer(f"{texts['Start_hello']}, {message.from_user.full_name}! {texts['text_message']}",
                             reply_markup=start(texts))
    elif user and not user.photo:  # Добавлена проверка user на None
        await message.answer(texts["main_menu"], reply_markup=start(texts))
    else:
        await message.answer(texts["welcome_message"], reply_markup=main(texts))


# Обработчик команды /help
async def command_help(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["about_bot"], reply_markup=helps(texts))


# Регистрация обработчиков команд
def register(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(command_help, commands='help')
    dp.register_message_handler(Language, commands='language')