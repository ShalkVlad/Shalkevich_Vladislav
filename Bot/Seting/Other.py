from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from Bot.DataBase import DB, Profil_vere
from Bot.Language.Language import get_user_texts, get_user_language, load_language_texts
from Bot.User_Keybord.User_kb import main, start, helps

router = Router()

# Декоратор для отмены
def cancel(func):
    async def cancel_registration(message: Message, state: FSMContext, *args, **kwargs):
        texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
        user_id = message.from_user.id
        user = DB.get_user(user_id)
        preferences = Profil_vere.get_user_preferences(user_id)

        if message.text.strip() == texts["cancelS"]:
            if not user.photo:
                await state.clear()
                await message.answer(texts["cancel_message"], reply_markup=start(texts))
            else:
                await state.clear()
                await message.answer(texts["cancel_message"], reply_markup=main(texts))
        elif message.text.strip() == texts["Cancel"]:
            await state.clear()
            await message.answer(texts["update_cancelled"], reply_markup=main(texts))
        else:
            await func(message, state, texts, preferences, user_id, *args, **kwargs)

    return cancel_registration

# Обработчик команды /start
@router.message(commands=["start"])
async def command_start(message: Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    user_id = message.from_user.id
    user = DB.get_user(user_id)

    if not DB.is_user_registered(user_id):
        DB.create_profile(user_id, "", 0, "", "", "", "", "", "", "Русский")
        await message.answer(f"{texts['Start_hello']}, {message.from_user.full_name}! {texts['text_message']}",
                             reply_markup=start(texts))
    elif user and not user.photo:
        await message.answer(texts["main_menu"], reply_markup=start(texts))
    else:
        await message.answer(texts["welcome_message"], reply_markup=main(texts))

# Обработчик команды /help
@router.message(commands=["help"])
async def command_help(message: Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["about_bot"], reply_markup=helps(texts))

# Регистрация всех обработчиков
def register(router: Router):
    router.message.register(command_start)
    router.message.register(command_help)
