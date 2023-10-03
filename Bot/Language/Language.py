import json

from aiogram import types

from DataBase import DB
from User_Keybord.User_kb import language, main


async def Language(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_language"], reply_markup=language)


def get_user_language(user_id: int, session: DB.Session):
    user = session.query(DB.User).filter_by(id=user_id).first()
    if user:
        return user.language
    return None


def get_user_texts(user_id, session):
    user_language = get_user_language(user_id, session)
    return load_language_texts(user_language)


def load_language_texts(languag):
    if not languag:
        languag = "Русский"
    with open(f"Language/{languag}.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Function to set the language to Belarusian
async def belarusian_language(message: types.Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Беларускі")
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["doneBelarusian"], reply_markup=main(texts))


# Function to set the language to Ukrainian
async def ukrainian_language(message: types.Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Українська")
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["doneUkrainian"], reply_markup=main(texts))


# Function to set the language to Polish
async def polish_language(message: types.Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Polski")
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["donePolish"], reply_markup=main(texts))


async def russian_language(message: types.Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "Русский")
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["doneRu"], reply_markup=main(texts))


async def english_language(message: types.Message):
    user_id = message.from_user.id
    await DB.update_user_language(user_id, "English")
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["doneEng"], reply_markup=main(texts))
