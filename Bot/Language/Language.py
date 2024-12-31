import json
from aiogram import Router
from aiogram.types import Message

from Bot.DataBase import DB
from Bot.User_Keybord.User_kb import main

router = Router()

# Обработчик команды для выбора языка
@router.message(commands=["language"])
async def language_command(message: Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_language"])

# Получение языка пользователя
def get_user_language(user_id: int, session: DB.Session):
    user = session.query(DB.User).filter_by(id=user_id).first()
    if user:
        return user.language
    return None

# Загрузка текстов на выбранном языке
def get_user_texts(user_id: int, session: DB.Session):
    user_language = get_user_language(user_id, session)
    return load_language_texts(user_language)

# Функция для загрузки языковых текстов
def load_language_texts(language: str):
    if not language:
        language = "Русский"
    with open(f"Language/{language}.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Функция для смены языка на белорусский
@router.message(lambda message: message.text == "Беларускі")
async def belarusian_language(message: Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Беларускі")
    texts = get_user_texts(user_id, DB.session)
    await message.answer(texts["doneBelarusian"], reply_markup=main(texts))

# Функция для смены языка на украинский
@router.message(lambda message: message.text == "Українська")
async def ukrainian_language(message: Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Українська")
    texts = get_user_texts(user_id, DB.session)
    await message.answer(texts["doneUkrainian"], reply_markup=main(texts))

# Функция для смены языка на польский
@router.message(lambda message: message.text == "Polski")
async def polish_language(message: Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Polski")
    texts = get_user_texts(user_id, DB.session)
    await message.answer(texts["donePolish"], reply_markup=main(texts))

# Функция для смены языка на русский
@router.message(lambda message: message.text == "Русский")
async def russian_language(message: Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Русский")
    texts = get_user_texts(user_id, DB.session)
    await message.answer(texts["doneRu"], reply_markup=main(texts))

# Функция для смены языка на английский
@router.message(lambda message: message.text == "English")
async def english_language(message: Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "English")
    texts = get_user_texts(user_id, DB.session)
    await message.answer(texts["doneEng"], reply_markup=main(texts))
