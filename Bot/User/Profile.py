import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ContentType
from geopy import Nominatim

from DataBase import DB, Profil_vere
from Language.Language import load_language_texts, get_user_language
from Seting.Creat_Bot import dp, bot
from Seting.Other import cancels
from User_Keybord.User_kb import Create, main, genders, location


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
async def process_name(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    name = message.text.strip()
    if not (3 <= len(name) <= 15) or not name.isalpha():
        await message.answer(texts["name_length_error"])
        return

    async with state.proxy() as data:
        data['name'] = name
        data['telegram_id'] = message.from_user.id
        if not preferences:
            await message.answer(texts["enter_age"], reply_markup=Create(texts))
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
        await message.answer(texts["invalid_age_value"])
        return

    if not (10 <= age <= 70):
        await message.answer(texts["age_range_error"])
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
@cancels
async def process_photo(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
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
        await message.answer(texts["upload_photo_error"])


@dp.message_handler(state=RegistrationState.photo)
@cancels
async def handle_text_input(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    await message.answer(texts["upload_photo_error"])


@dp.message_handler(state=RegistrationState.gender)
@cancels
async def process_gender(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    gender = message.text

    valid_genders = [texts["male"], texts["female"], texts["other"], "♂️", "♀️", "🤖"]

    if gender not in valid_genders:
        await message.answer(texts["select_gender_error"].format(", ".join(valid_genders)))
        return

    async with state.proxy() as data:
        data['gender'] = gender

        if not preferences:
            await message.answer(texts["enter_country"], reply_markup=location(texts))
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
    await message.answer(texts["select_gender_error"])


@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.TEXT], state=RegistrationState.country)
async def process_location_or_text(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    user_id = message.from_user.id
    preferences = Profil_vere.get_user_preferences(user_id)
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    user_id = message.from_user.id
    preferences = Profil_vere.get_user_preferences(user_id)

    async with state.proxy() as data:
        if message.content_type == ContentType.LOCATION:
            latitude = message.location.latitude
            longitude = message.location.longitude
            geolocator = Nominatim(user_agent="MYBOTs")
            try:
                locations = geolocator.reverse((latitude, longitude), language="ru")
                country = locations.raw["address"].get("country")
                city = locations.raw["address"].get("city")

                data['country'] = country
                data['city'] = city

                await message.answer(f"{texts['your_country']} {country},{texts['your_city']} {city}")

                if not preferences:
                    await message.answer(texts["about_prompt"], reply_markup=Create(texts))
                    await RegistrationState.about.set()
                else:
                    await DB.update_user_profile(user_id, {"country": country, "city": city})

                    await state.finish()
                    await message.answer(texts["update_successful"])
                    await message.answer(texts["welcome_message"], reply_markup=main(texts))
            except Exception as e:
                logging.error(f"Error during reverse geocoding: {e}")
                await message.answer(texts["geolocation_error"])
        else:
            if 'country' not in data:
                location_input = message.text.strip()
                if not location_input.isalpha():
                    await message.answer(texts["invalid_country_name"])
                else:
                    data['country'] = location_input
                    await message.answer(f"{texts['your_country']} {data['country']}")

                    await message.answer(texts["enter_city"])
            else:
                city_input = message.text.strip()
                if not city_input.isalpha():
                    await message.answer(texts["invalid_city_name"])
                else:
                    data['city'] = city_input

                    if not preferences:
                        await message.answer(texts["about_prompt"], reply_markup=Create(texts))
                        await RegistrationState.about.set()
                    else:
                        await DB.update_user_profile(user_id, {"country": data['country'], "city": city_input})

                        await state.finish()
                        await message.answer(texts["update_successful"])
                        await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(state=RegistrationState.about)
@cancels
async def process_about(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
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
        await message.answer(f"{texts['congratulations']}, {name}!\n"
                             f"{texts['profile_created_success']}\n"
                             f"{texts['your_data']}\n"
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
