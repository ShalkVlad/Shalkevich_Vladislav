import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ContentType
from geopy import Nominatim

import DB
from Creat_Bot import dp, bot
from DB import create_profile
from User_kb import gender_markup, main_keyboard, location_keyboard


class RegistrationState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    country = State()
    city = State()
    about = State()
    photo = State()


class Newdata(StatesGroup):
    photo = State()
    name = State()
    age = State()
    country = State()
    city = State()
    about = State()


@dp.message_handler(state=RegistrationState.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not (3 <= len(name) <= 15):
        await message.answer("Имя должно содержать от 3 до 15 символов. Пожалуйста, попробуйте еще раз.")
        return

    if not name.isalpha():
        await message.answer("Имя может содержать только буквы. Пожалуйста, попробуйте еще раз.")
        return

    async with state.proxy() as data:
        data['name'] = name

    await message.answer("Введите ваш возраст")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.reply("Пожалуйста, введите корректное значение возраста (целое число).")
        return

    if not (0 <= age <= 60):
        await message.answer("Возраст должен быть от 0 до 60 лет. Пожалуйста, попробуйте еще раз.")
        return

    async with state.proxy() as data:
        data['age'] = age

    await message.answer("Теперь загрузите вашу фотографию")
    await RegistrationState.photo.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=RegistrationState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    # Получаем файл фотографии из сообщения
    photo = message.photo[-1].file_id

    async with state.proxy() as data:
        data['photo'] = photo

    await message.answer("Выберите ваш пол", reply_markup=gender_markup)
    await RegistrationState.gender.set()


@dp.message_handler(lambda message: message.text in ["♂️ Мужской", "♀️ Женский", "🤖 Другое", "♂️", "♀️", "🤖"],
                    state=RegistrationState.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text

    if gender not in ["♂️ Мужской", "♀️ Женский", "🤖 Другое", "♂️", "♀️", "🤖"]:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов")
        return

    async with state.proxy() as data:
        data['gender'] = gender

    await message.answer("Введите вашу страну", reply_markup=location_keyboard)
    await RegistrationState.country.set()


@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.TEXT], state=RegistrationState.country)
async def process_country_input_or_location(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.LOCATION:
        latitude = message.location.latitude
        longitude = message.location.longitude

        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse((latitude, longitude), language="ru")
        country = location.raw["address"].get("country")
        city = location.raw["address"].get("city")

        async with state.proxy() as data:
            data['country'] = country
            data['city'] = city

        await message.answer(f"Ваша страна: {country}")
        await message.answer(f"Ваш город: {city}")
        await message.answer("Расскажите немного о себе", reply_markup=ReplyKeyboardRemove())
        await RegistrationState.about.set()
    else:
        country = message.text.strip()
        async with state.proxy() as data:
            data['country'] = country

        await message.answer("Укажите ваш город")
        await RegistrationState.city.set()


@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.TEXT], state=RegistrationState.city)
async def process_city_input_or_location(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.LOCATION:
        latitude = message.location.latitude
        longitude = message.location.longitude

        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse((latitude, longitude), language="ru")
        city = location.raw["address"].get("city")
    else:
        city = message.text.strip()

    async with state.proxy() as data:
        data['city'] = city

    await message.answer(f"Ваш город: {city}")
    await message.answer("Расскажите немного о себе", reply_markup=ReplyKeyboardRemove())
    await RegistrationState.about.set()


@dp.message_handler(state=RegistrationState.about)
async def process_about(message: types.Message, state: FSMContext):
    about = message.text.strip()

    async with state.proxy() as data:
        data['about'] = about

    user_id = message.from_user.id
    name = data["name"]
    age = data["age"]
    gender = data["gender"]
    country = data["country"]
    city = data["city"]
    about = data["about"]
    photo = data["photo"]

    create_profile(user_id, name, age, gender, country, about, photo, city)
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer(f"🎉 Поздравляем, {name}!\n"
                         f"Ваша анкета успешно создана!\n"
                         f"Ваши данные:\n"
                         f"Имя: {name}, Возраст: {age}, Пол: {gender}\n"
                         f"Страна: {country}, Город: {city}\n"
                         f"Информация о себе: {about}\n",
                         reply_markup=ReplyKeyboardRemove())

    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)


@dp.message_handler(state=Newdata.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not (3 <= len(name) <= 15):
        await message.answer("Имя должно содержать от 3 до 15 символов. Пожалуйста, попробуйте еще раз.")
        return

    if not name.isalpha():
        await message.answer("Имя может содержать только буквы. Пожалуйста, попробуйте еще раз.")
        return
    user_id = message.from_user.id
    result = await asyncio.to_thread(DB.update_user_name, user_id, name)

    if result:
        await message.reply("Имя успешно обновлено!")
    else:
        await message.reply("Произошла ошибка при обновлении имени.")

    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)


@dp.message_handler(state=Newdata.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.reply("Пожалуйста, введите корректное значение возраста (целое число).")
        return

    if not (0 <= age <= 60):
        await message.answer("Возраст должен быть от 0 до 60 лет. Пожалуйста, попробуйте еще раз.")
        return

    user_id = message.from_user.id
    result = await asyncio.to_thread(DB.update_user_age, user_id, age)

    if result:
        await message.reply("Возраст успешно обновлен!")
    else:
        await message.reply("Произошла ошибка при обновлении возраста.")

    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)


@dp.message_handler(content_types=ContentType.PHOTO, state=Newdata.photo)
async def process_photo(message: types.Message, state: FSMContext):
    # Получаем файл фотографии из сообщения
    photo = message.photo[-1].file_id

    user_id = message.from_user.id
    if await DB.update_user_photo(user_id, photo):
        # Фотография успешно обновлена в базе данных
        await bot.send_message(chat_id=message.chat.id, text="Фотография успешно обновлена!")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
    else:
        # Произошла ошибка при обновлении фотографии
        await bot.send_message(chat_id=message.chat.id, text="Произошла ошибка при обновлении фотографии.")

    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)


@dp.message_handler(state=Newdata.about)
async def process_about_me(message: types.Message, state: FSMContext):
    about_me = message.text
    user_id = message.from_user.id
    result = await asyncio.to_thread(DB.update_user_about, user_id, about_me)

    if result:
        await message.reply("Информация о себе успешно обновлена!")
    else:
        await message.reply("Произошла ошибка при обновлении информации о себе.")

    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)


@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.TEXT], state=Newdata.country)
async def process_country_input_or_location(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.LOCATION:
        latitude = message.location.latitude
        longitude = message.location.longitude

        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse((latitude, longitude), language="ru")
        country = location.raw["address"].get("country")
    else:
        country = message.text.strip()

    async with state.proxy() as data:
        data['country'] = country

    await message.answer(f"Ваша страна: {country}")
    await message.answer("Укажите ваш город или нажмите на кнопку '📍 Предоставить геолокацию'",
                         reply_markup=location_keyboard)
    await RegistrationState.city.set()


@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.TEXT], state=Newdata.city)
async def process_city_input_or_location(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.LOCATION:
        latitude = message.location.latitude
        longitude = message.location.longitude

        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse((latitude, longitude), language="ru")
        city = location.raw["address"].get("city")
    else:
        city = message.text.strip()

    async with state.proxy() as data:
        data['city'] = city

    await message.reply(f"Ваш город: {city}. Город успешно обновлен!")

    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)


@dp.message_handler(state=Newdata.country)
async def process_country(message: types.Message, state: FSMContext):
    country = message.text
    user_id = message.from_user.id
    result = await asyncio.to_thread(DB.update_user_country, user_id, country)

    if result:
        await message.reply(f"Ваша страна: {country}. Страна успешно обновлена!")
    else:
        await message.reply("Произошла ошибка при обновлении страны.")

    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)
