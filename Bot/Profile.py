import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ContentType
from geopy import Nominatim

import DB
from Creat_Bot import dp, bot
from Other import load_language_texts, get_user_language, cancels
from User_kb import genders, main, location, Create


class RegistrationState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    country = State()
    city = State()
    about = State()
    photo = State()


@dp.message_handler(state=RegistrationState.name)
@cancels
async def process_name(message: types.Message, state: FSMContext,texts, preferences, user_id, raw_state):
    name = message.text.strip()
    if not (3 <= len(name) <= 15) or not name.isalpha():
        await message.answer(texts["VAllUE-NAME"])
        return

    async with state.proxy() as data:
        data['name'] = name
        data['telegram_id'] = message.from_user.id
        if not preferences:
            await message.answer(texts["AGE"], reply_markup=Create(texts))
            await RegistrationState.age.set()
        else:
            # Просто передайте имя напрямую в функцию обновления профиля
            await DB.update_user_profile(user_id, {"name": name})
            await state.finish()
            await message.answer(texts["update_successful"])
            await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(state=RegistrationState.age)
@cancels
async def process_age(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer(texts["VAllUE-AGE"])
        return

    if not (10 <= age <= 70):
        await message.answer(texts["TRABLE-AGE"])
        return

    async with state.proxy() as data:
        data['age'] = age

    if not preferences:
        await message.answer(texts["photo_prompt"], reply_markup=Create(texts))
        await RegistrationState.photo.set()
    else:
        # Просто передайте имя напрямую в функцию обновления профиля
        await DB.update_user_profile(user_id, {"age": age})
        await state.finish()
        await message.answer(texts["update_successful"])
        await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(content_types=ContentType.PHOTO, state=RegistrationState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    user_id = message.from_user.id
    user = DB.get_user(user_id)
    preferences = user.about
    if message.content_type == ContentType.PHOTO:
        photo = message.photo[-1].file_id

        async with state.proxy() as data:
            data['photo'] = photo

        if not preferences:
            await message.answer((texts["gender_prompt"]), reply_markup=genders(texts))
            await RegistrationState.gender.set()
        else:
            # Просто передайте имя напрямую в функцию обновления профиля
            await DB.update_user_profile(user_id, {"photo": photo})
            await state.finish()
            await message.answer(texts["update_successful"])
            await message.answer(texts["welcome_message"], reply_markup=main(texts))
    else:
        await message.answer(texts["VAllUE-PHOTO"])


@dp.message_handler(state=RegistrationState.photo)
async def handle_text_input(message: types.Message):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    await message.answer(texts["VAllUE-PHOTO"])


@dp.message_handler(state=RegistrationState.gender)
@cancels
async def process_gender(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):

    gender = message.text

    valid_genders = [texts["male"], texts["female"], texts["other"], "♂️", "♀️", "🤖"]

    if gender not in valid_genders:
        await message.answer(texts["VAllUE-GENDER"].format(", ".join(valid_genders)))
        return

    async with state.proxy() as data:
        data['gender'] = gender

        if not preferences:
            await message.answer(texts["location_prompt"], reply_markup=location(texts))
            await RegistrationState.country.set()
        else:
            # Просто передайте имя напрямую в функцию обновления профиля
            await DB.update_user_profile(user_id, {"gender": gender})
            await state.finish()
            await message.answer(texts["update_successful"])
            await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(content_types=ContentType.TEXT, state=RegistrationState.gender)
async def process_gender_text(message: types.Message):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    await message.answer(texts["TRABLE-GENDER"])


@dp.message_handler(lambda message: message.content_type in [ContentType.LOCATION, ContentType.TEXT],
                    state=RegistrationState.country)
@cancels
async def process_location_or_city_input(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    async with state.proxy() as data:
        if message.content_type == ContentType.LOCATION:
            latitude = message.location.latitude
            longitude = message.location.longitude
            geolocator = Nominatim(user_agent="PhysioGnomySBOT")

            try:
                locations = geolocator.reverse((latitude, longitude), language="ru")
                country = locations.raw["address"].get("country")
                city = locations.raw["address"].get("city")

                if data.get('country') is None:
                    data['country'] = country
                    await message.answer(texts["USER_COUNTRY"] + country)
                if data.get('city') is None:
                    data['city'] = city
                    await message.answer(texts["USER_CITY"] + city)
                    if not preferences:
                        await message.answer(texts["about_prompt"], reply_markup=Create(texts))
                        await RegistrationState.about.set()
                    else:
                        # Просто передайте имя напрямую в функцию обновления профиля
                        await DB.update_user_profile(user_id, {"country": country})
                        await DB.update_user_profile(user_id, {"city": city})
                        await state.finish()
                        await message.answer(texts["update_successful"])
                        await message.answer(texts["welcome_message"], reply_markup=main(texts))

                await message.answer(texts["about_prompt"], reply_markup=Create(texts))
                await RegistrationState.about.set()
            except Exception as e:
                logging.error(f"Ошибка при обратном геокодировании: {e}")
                await message.answer(texts["TRABLE_CITY"])
        else:
            async with state.proxy() as data:
                if 'country' not in data:
                    location_input = message.text.strip()
                    if not location_input.isalpha():
                        await message.answer(texts["TRABLE_COUNTRY_NAME"])
                        return
                    data['country'] = location_input

                    await message.answer(
                        f"{texts['USER_COUNTRY']} {data['country']}")
                    if not preferences:
                        await message.answer(texts["CITY_PARTNER"], reply_markup=Create(texts))
                        await RegistrationState.city.set()
                    else:
                        # Просто передайте имя напрямую в функцию обновления профиля
                        await DB.update_user_profile(user_id, {"country": location_input})
                        await state.finish()
                        await message.answer(texts["update_successful"])
                        await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(lambda message: message.content_type == ContentType.TEXT, state=RegistrationState.city)
@cancels
async def process_text_location_input(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    async with state.proxy() as data:
        city_input = message.text.strip()
        if not city_input.isalpha():
            await message.answer(texts["TRABLE_CITY_NAME"])
            return
        data['city'] = city_input
        await message.answer( f"{texts['USER_CITY']}:{city_input}")
        if not preferences:
            await message.answer(texts["about_prompt"], reply_markup=Create(texts))
            await RegistrationState.about.set()
        else:
            # Просто передайте имя напрямую в функцию обновления профиля
            await DB.update_user_profile(user_id, {"city": city_input})
            await state.finish()
            await message.answer(texts["update_successful"])
            await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(state=RegistrationState.about)
@cancels
async def process_about(message: types.Message, state: FSMContext, texts, preferences, user_id,  raw_state):
    about = message.text.strip()
    if not preferences:
        async with state.proxy() as data:
            data['about'] = about
            telegram_username = message.from_user.username
            user_id = message.from_user.id
        name = data["name"]
        age = data["age"]
        gender = data["gender"]
        country = data["country"]
        city = data["city"]
        about = data["about"]
        photo = data["photo"]
        language = get_user_language(user_id, DB.session)

        DB.update_profile(user_id, name, age, gender, country, about, photo, city, telegram_username, language)
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        await message.answer(f"{texts['G']}, {name}!\n"
                             f"{texts['R']}\n"
                             f"{texts['E']}\n"
                             f"{name}, {age}, {texts['gender']}: {gender}\n"
                             f"{texts['country']} {country}, {texts['city']}  {city}\n"
                             f"{about}\n",
                             reply_markup=ReplyKeyboardRemove())

        await state.finish()
        await message.answer(texts["welcome_message"], reply_markup=main(texts))
    else:
        # Просто передайте имя напрямую в функцию обновления профиля
        await DB.update_user_profile(user_id, {"about": about})
        await state.finish()
        await message.answer(texts["update_successful"])
        await message.answer(texts["welcome_message"], reply_markup=main(texts))
