import logging
import os

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType, ReplyKeyboardRemove
from deepface import DeepFace
from geopy import Nominatim

from DataBase import Profil_vere, DB
from DataBase.Profil_vere import get_user_preferences
from Language.Language import load_language_texts, get_user_language, get_user_texts
from Seting.Config import TOKEN
from Seting.Creat_Bot import dp, bot
from Seting.Other import cancel
from User import search
from User_Keybord.User_kb import genders, main, location


class ProfileState(StatesGroup):
    preferred_country = State()
    preferred_gender = State()
    confirmed = State()
    preferred_age = State()
    preferred_city = State()


@dp.message_handler(state=ProfileState.preferred_age)
@cancel
async def process_age(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    async with state.proxy() as data:
        if 'min_age' not in data:
            try:
                age = int(message.text)
                if not (10 <= age <= 70):
                    raise ValueError(texts["age_range_error"])
            except ValueError:
                await message.answer(texts["age_range_error"])
                return
            data['min_age'] = age
            await message.answer(texts["max_age_prompt"])
        else:
            try:
                max_age = int(message.text)
                if not (10 <= max_age <= 71):
                    await message.answer(texts["age_range_error"])
                if max_age <= data['min_age']:
                    raise ValueError(texts["invalid_age_range"])
            except ValueError:
                await message.answer(texts["age_range_error"])
                return
            data['max_age'] = max_age
            preferences_dict = {
                "preferred_age_min": data['min_age'],
                "preferred_age_max": data['max_age'],
            }
            if not preferences:
                await message.answer(texts["partner_gender_prompt"], reply_markup=genders(texts))
                await ProfileState.preferred_gender.set()
            else:
                Profil_vere.update_user_preference(user_id, preferences_dict)
                await state.finish()
                await message.answer(texts["update_successful"])
                await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(state=ProfileState.preferred_gender)
@cancel
async def process_gender(message: types.Message, state: FSMContext, texts, preferences, user_id, raw_state):
    gender = message.text
    valid_genders = [texts["male"], texts["female"], texts["other"], "♂️", "♀️", "🤖"]
    if gender not in valid_genders:
        await message.answer(texts["select_gender_error"].format(", ".join(valid_genders)))
        return

    async with state.proxy() as data:
        data['gender'] = gender
        preferences_dict = {
            "preferred_gender": data['gender'],
        }
    if not preferences:
        await message.answer(texts["partner_country_prompt"], reply_markup=location(texts))
        await ProfileState.preferred_country.set()
    else:
        Profil_vere.update_user_preference(user_id, preferences_dict)
        await state.finish()
        await message.answer(texts["update_successful"])
        await message.answer(texts["welcome_message"], reply_markup=main(texts))


@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.TEXT],
                    state=[ProfileState.preferred_country, ProfileState.preferred_city])
async def process_location_or_text(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    async with state.proxy() as data:
        if message.content_type == ContentType.LOCATION:
            latitude = message.location.latitude
            longitude = message.location.longitude
            geolocator = Nominatim(user_agent="Geocoder")
            try:
                locations = geolocator.reverse((latitude, longitude), language="ru")
                country = locations.raw["address"].get("country")
                city = locations.raw["address"].get("city")

                if data.get('country') is None:
                    data['country'] = country
                if data.get('city') is None:
                    data['city'] = city
                    await message.answer(texts["search_country"] + country + " " + city)

                await message.answer(texts["send_photo_for_verification"], reply_markup=ReplyKeyboardRemove())

                await ProfileState.confirmed.set()
            except Exception as e:
                logging.error(f"Ошибка при обратном геокодировании: {e}")
                await message.answer(texts["geolocation_error"])
        else:
            if 'country' not in data:
                location_input = message.text.strip()
                if not location_input.isalpha():
                    await message.answer(texts["invalid_country_name"])
                    return
                data['country'] = location_input
                await message.answer(texts["partner_city_prompt"])
            else:
                city_input = message.text.strip()
                if not city_input.isalpha():
                    await message.answer(texts["invalid_country_name"])
                    return
                data['city'] = city_input

                await message.answer(
                    f"{texts['serch_preper']}:{data['country']}, {texts['USER_CITY']}:{city_input}")

                await message.answer(texts["send_photo_for_verification"], reply_markup=ReplyKeyboardRemove())
                await ProfileState.confirmed.set()


@dp.message_handler(state=ProfileState.confirmed)
async def handle_text_input(message: types.Message):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    await message.answer(texts["upload_photo_error"])


async def verify_face(img1, img2):
    try:
        result_dict = DeepFace.verify(img1_path=img1, img2_path=img2)
        return result_dict["verified"]
    except Exception as _ex:
        print(_ex)
        return False


@dp.message_handler(content_types=types.ContentType.PHOTO, state=ProfileState.confirmed)
async def process_user_photo(message: types.Message, state: FSMContext, raw_state):
    texts = get_user_texts(message.from_user.id, DB.session)
    print("Processing user photo:", message.from_user.id, message.photo)
    async with state.proxy() as data:
        user_id = message.from_user.id
        user_preferences = get_user_preferences(user_id)
        user_photo = message.photo[-1]
        user_photo_url = await user_photo.get_url()
        user_profile = DB.get_user(user_id)
        if user_profile is None:
            await message.answer(texts["profile_not_found_error"])
            return
        profile_photo_id = user_profile.photo
        profile_photo_info = await bot.get_file(profile_photo_id)
        profile_photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{profile_photo_info.file_path}"
        async with aiohttp.ClientSession() as session:
            async with session.get(user_photo_url) as user_photo_response:
                user_photo_data = await user_photo_response.read()
            async with session.get(profile_photo_url) as profile_photo_response:
                profile_photo_data = await profile_photo_response.read()
        save_path = r"C:\Users\shalk\PycharmProjects\pythonProject1\photos"
        os.makedirs(save_path, exist_ok=True)
        user_photo_file_name = "user_uploaded_photo.jpg"
        user_photo_full_file_path = os.path.join(save_path, user_photo_file_name)
        profile_photo_file_name = "user_profile_photo.jpg"
        profile_photo_full_file_path = os.path.join(save_path, profile_photo_file_name)
        with open(user_photo_full_file_path, 'wb') as user_photo_f:
            user_photo_f.write(user_photo_data)
        with open(profile_photo_full_file_path, 'wb') as profile_photo_f:
            profile_photo_f.write(profile_photo_data)
        data.setdefault('confirmed', False)
        verification_result = await verify_face("photos/user_profile_photo.jpg", "photos/user_uploaded_photo.jpg")
        if verification_result:
            await message.answer(texts["photo_match_success"])
            if user_preferences:
                user_preferences.confirmed = True
            data['confirmed'] = True
            preferences = {
                "gender": data['gender'],
                "min_age": data['min_age'],
                "max_age": data['max_age'],
                "country": data['country'],
                "city": data['city'],
                "confirmed": data['confirmed']
            }
            Profil_vere.save_user_preferences(user_id, preferences)
            Profil_vere.session.commit()
        else:
            await message.answer(texts["photo_match_failure"])
            preferences = {
                "gender": data['gender'],
                "min_age": data['min_age'],
                "max_age": data['max_age'],
                "country": data['country'],
                "city": data['city'],
                "confirmed": data['confirmed']
            }
            Profil_vere.save_user_preferences(user_id, preferences)
            Profil_vere.session.commit()
        await message.answer(texts["great_results"])
        await state.finish()
        await search.ProfileLookupState.show_next.set()
        await search.process_profile_lookup(message, state)
