import json
import string

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ContentType

import db
from creat_Bot import dp, bot
from db import create_profile
from user_kb import But_User_Help, But_User_start, gender_markup, keyboard, keyboard_bonus


class RegistrationState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()


async def exo(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('Black.json')))) != set():
        await message.reply("Мат запрещён")
        await message.delete()
    elif message.text == "👋 Создать Анкету" or message.text == "👋":
        user_id = message.from_user.id
        if db.is_user_registered(user_id):
            await message.answer("У вас уже есть анкета, хотите изменить её?", reply_markup=ReplyKeyboardRemove())
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=keyboard)
        else:
            await message.answer("Отлично! Давай начнем создание анкеты. Как тебя зовут?",
                                 reply_markup=ReplyKeyboardRemove())
            await RegistrationState.name.set()
    elif message.text == "❓ Информация о боте" or message.text == "❓":
        await message.answer("Выберете ваш вопрос", reply_markup=But_User_Help)
    elif message.text == "📜 Правила сообщества":
        await message.answer("Значит правил в нашем боте не много):\n1.Не вздумай скидывать сюда пошлятину, "
                             "я предупредил)\n2.Будь вежлив , имей уважение к собеседнику)\n3.Нарушение правил "
                             "строго наказывается , а если точнее то вас Забанят ")
    elif message.text == "🤔 Что я могу?":
        await message.answer("У меня еще не много функций😔,но я могу например найти тебе пару), а возможно и "
                             "две пары, или даже три) или забанить тебя за плохое поведение! Но я надеюсь этого "
                             "не будет:) ")
    elif message.text == "💰 Кошелёк" or message.text == "💰":
        await message.answer("За душой ни гроша")
    elif message.text == "❤️ Взаимные симпатии" or message.text == "❤️":
        await message.answer("У тебя есть моя симпатия 😉")
    elif message.text == "👀 Смотреть анкеты" or message.text == "👀":
        await message.answer("В разработке")
    elif message.text == "🌐 Сменить язык" or message.text == "🌐":
        await message.answer("Ю Спык инглиш?)")
    elif message.text == "🏠 главное меню" or message.text == "🏠":
        user_id = message.from_user.id
        if db.is_user_registered(user_id):
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=keyboard)
    elif message.text == "🔙 Вернуться в главное меню" or message.text == "🔙":
        user_id = message.from_user.id
        if db.is_user_registered(user_id):
            await message.answer("Если нужна будет помошь, обращайся)", reply_markup=ReplyKeyboardRemove())
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=keyboard)
        else:
            await message.answer("Вы вернулись в главное меню", reply_markup=But_User_start)
    elif message.text == "😊 Моя анкета" or message.text == "😊":
        user_id = message.from_user.id
        profile = db.get_profile(user_id)
        if profile:
            name, age, gender = profile
            photo_data = db.get_user_photo(user_id)
            if photo_data:
                await bot.send_photo(chat_id=message.chat.id, photo=photo_data)
            text = f"Имя: {name}\n Возраст: {age}\n Пол: {gender}"
            await bot.send_message(chat_id=message.chat.id, text=text)
        else:
            text = "Профиль не найден"
            await bot.send_message(chat_id=message.chat.id, text=text)
    elif message.text == "🎁 Бонусы" or message.text == "🎁":
        await message.answer("⭐️ Звезда\n💬 Напиши 'Привет'\n👑 Персона ВИП\n👤 Инкогнито\n💪🏼 НЕТ ЛИМИТУ! … Почти",
                             reply_markup=keyboard_bonus)
        if message.text == "⭐️ Звезда" or message.text == "⭐️":
            await message.answer("Наделяет тебя невероятной удачей, анкета выпадает чаще и всегда на виду стоимость 600"
                                 " баллов срок 7 дней, 1100 баллов стоимость за месяц ")
        elif message.text == "💬 Напиши 'Привет'" or message.text == "💬":
            await message.answer("Открывает для тебя не только оценить, но и написать понравившемуся пользователю "
                                 "сообщение (Стоимость 800 баллов срок 7 дней, 1500 баллов за месяц)")
        elif message.text == "👑 Персона ВИП" or message.text == "👑":
            await message.answer("Перед вами открыты все двери, всё внимание и персональный отбор анкет, для вас нет "
                                 "границ. Вы персона ВИП)")
        elif message.text == "👤‍ Инкогнито" or message.text == "👤":
            await message.answer("Вы таинственны, загадочны и можете раскрыть свою личность лишь тем, кого посчитайте"
                                 " достойным")
        elif message.text == "💪🏼 НЕТ ЛИМИТУ! … Почти" or message.text == "💪🏼":
            await message.answer("Существующий лимит кажется слишком маленьким? Для тебя уникальное предложение "
                                 "увеличь количества анкет.")
    else:
        await message.answer("что?")


@dp.message_handler(state=RegistrationState.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name.isalpha():
        await message.answer("Имя может содержать только буквы. Попробуйте еще раз.")
        return

    async with state.proxy() as data:
        data['name'] = name

    await message.answer("Введите ваш возраст")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введите возраст цифрами")
        return

    async with state.proxy() as data:
        data['age'] = age

    await message.answer("Выберите ваш пол", reply_markup=gender_markup)
    await RegistrationState.gender.set()


@dp.message_handler(lambda message: message.text in ["♂️ Мужчина", "♀️ Женщина", "🤖 Другое", "♂️", "♀️", "🤖"],
                    state=RegistrationState.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text

    if gender not in ["♂️ Мужчина", "♀️ Женщина", "🤖 Другое", "♂️", "♀️", "🤖"]:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов")
        return

    async with state.proxy() as data:
        data['gender'] = gender

    await message.answer("Пришлите свою фотографию")
    await RegistrationState.photo.set()

    async with state.proxy() as data:
        data['photo'] = None


@dp.message_handler(content_types=ContentType.PHOTO, state=RegistrationState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    async with state.proxy() as data:
        data['photo'] = photo
    await message.answer("Фотография успешно сохранена")
    await state.finish()

    user_id = message.from_user.id
    name = data["name"]
    age = data["age"]
    gender = data["gender"]
    photo = data['photo']

    create_profile(user_id, name, age, gender, photo)
    await message.answer(f"🎉 Поздравляем, {name}!\n"
                         f"Ваша анкета успешно создана!\n"
                         f"Ваши данные:\n"
                         f"Имя: {name}\n"
                         f"Возраст: {age}\n"
                         f"Пол: {gender}",
                         reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=keyboard)


def reg_other(dp: Dispatcher):
    dp.register_message_handler(exo)
    dp.register_message_handler(process_name, state=RegistrationState.name)
    dp.register_message_handler(process_age, state=RegistrationState.age)
    dp.register_callback_query_handler(process_gender, state=RegistrationState.gender)
