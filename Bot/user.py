import json
import string

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ContentType

import Profil
import db
from creat_Bot import bot
from user_kb import help_keyboard, main_keyboard, start_keyboard, edit_profile_keyboard, \
    edit_profile_keyboard_with_fields, bonus_keyboard


async def process_message(message: types.Message):
    # Check for specific commands
    commands = {
        "👋 Создать Анкету", "👋", "❓ Информация о боте", "❓", "📜 Правила сообщества", "🤔 Что я могу?",
        "💰 Кошелёк", "💰", "❤️ Взаимные симпатии", "❤️", "👀 Смотреть анкеты", "👀", "🌐 Сменить язык", "🌐",
        "🔙 Вернуться в главное меню", "🔙", "😊 Моя анкета", "😊", "✏️ Изменить анкету", "✏️", "📷 Изменить фото",
        "📷", "😀 Изменить имя", "😀", "🎂 Изменить возраст", "🎂", "🌎 Изменить страну", "🌎", "✍️ Изменить описание",
        "✍️", "❌ Удалить анкету", "❌", "🆕 Новая анкета", "🆕", "🏠 Главное меню", "🏠", "🎁 Бонусы", "🎁",
        "⭐️ Звезда", "⭐️", "💬 Напиши 'Привет'", "💬", "👑 Персона ВИП", "👑", "👤‍ Инкогнито", "👤",
        "💪🏼 НЕТ ЛИМИТУ! … Почти", "💪🏼", "🏠 главное меню", "🏠"
    }

    if message.text in commands:
        # Process commands
        await process_commands(message)
    else:
        # Handle other text messages
        await process_text_message(message)


async def process_commands(message: types.Message):
    if message.text == "👋 Создать Анкету" or message.text == "👋":
        user_id = message.from_user.id
        if db.is_user_registered(user_id):
            await message.answer("У вас уже есть анкета, хотите изменить её?", reply_markup=ReplyKeyboardRemove())
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=main_keyboard)
        else:
            await message.answer("Отлично! Давай начнем создание анкеты. Как тебя зовут?",
                                 reply_markup=ReplyKeyboardRemove())
            await Profil.RegistrationState.name.set()
    elif message.text == "❓ Информация о боте" or message.text == "❓":
        await message.answer("Выберете ваш вопрос", reply_markup=help_keyboard)
    elif message.text == "📜 Правила сообщества":
        await message.answer("Значит правил в нашем боте не много):\n1.Не вздумай скидывать сюда пошлятину, "
                             "я предупредил)\n2.Будь вежлив , имей уважение к собеседнику)\n3.Нарушение правил "
                             "строго наказывается , а если точнее то вас Забанят ")
    elif message.text == "🤔 Что я могу?":
        await message.answer("У меня еще не много функций😔,но я могу например найти тебе пару), а возможно и "
                             "две пары, или даже три) или забанить тебя за плохое поведение! Но я надеюсь этого "
                             "не будет:) ")
    elif message.text == "💰 Кошелёк" or message.text == "💰":
        user_id = message.from_user.id
        wallet = db.get_user_wallet(user_id)
        if wallet is not None:
            response = f"Ваш текущий баланс: {wallet} единиц, хотите пополнить счёт?"
        else:
            response = "К сожалению, у вас нет кошелька"
        await message.answer(response)
    elif message.text == "❤️ Взаимные симпатии" or message.text == "❤️":
        await message.answer("У тебя есть моя симпатия 😉")
    elif message.text == "👀 Смотреть анкеты" or message.text == "👀":
        await message.answer("В разработке")
    elif message.text == "🌐 Сменить язык" or message.text == "🌐":
        await message.answer("Ю Спык инглиш?)")
    elif message.text == "🔙 Вернуться в главное меню" or message.text == "🔙":
        user_id = message.from_user.id
        if db.is_user_registered(user_id):
            await message.answer("Если нужна будет помошь, обращайся)", reply_markup=ReplyKeyboardRemove())
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=main_keyboard)
        else:
            await message.answer("Вы вернулись в главное меню", reply_markup=start_keyboard)
    elif message.text == "😊 Моя анкета" or message.text == "😊":
        user_id = message.from_user.id
        profile = db.get_profile(user_id)
        if profile:
            name, age, gender, country, about, photo, wallet = profile
            text = f"Имя: {name}\nВозраст: {age}\nПол: {gender}\nСтрана: {country}\n" \
                   f"Баллы: {wallet}\nИнформация о себе: {about}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=edit_profile_keyboard)
        else:
            text = "Профиль не найден"
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard)
    elif message.text == "✏️ Изменить анкету" or message.text == "✏️":
        await message.answer("Какие данные вы хотите изменить?", reply_markup=edit_profile_keyboard_with_fields)
    elif message.text == "📷 Изменить фото" or message.text == "📷":
        await message.answer("Хорошо! Пришлите новую фотографию для вашей анкеты:", reply_markup=ReplyKeyboardRemove())
        await Profil.Newdata.photo.set()
    elif message.text == "😀 Изменить имя" or message.text == "😀":
        await message.answer("Введите ваше новое имя:")
        await Profil.Newdata.name.set()
    elif message.text == "🎂 Изменить возраст" or message.text == "🎂":
        await message.answer("Введите ваш новый возраст (целое число):")
        await Profil.Newdata.age.set()
    elif message.text == "🌎 Изменить страну" or message.text == "🌎":
        await message.answer("Введите вашу новую страну:")
        await Profil.Newdata.country.set()
    elif message.text == "✍️ Изменить описание" or message.text == "✍️":
        await message.answer("Введите ваше новое описание:")
        await Profil.Newdata.about.set()
    elif message.text == "❌ Удалить анкету" or message.text == "❌":
        user_id = message.from_user.id
        db.delete_profile(user_id)
        await message.answer("Ваша анкета была успешно удалена.", reply_markup=start_keyboard)
    elif message.text == "🆕 Новая анкета" or message.text == "🆕":
        user_id = message.from_user.id
        db.delete_profile(user_id)
        await message.answer("Отлично! Давай начнем создание анкеты. Как тебя зовут?",
                             reply_markup=ReplyKeyboardRemove())
        await Profil.RegistrationState.name.set()
    elif message.text == "🏠 Главное меню" or message.text == "🏠":
        await message.answer("Добро пожаловать в ваш персональный кабинет!", reply_markup=main_keyboard)
    elif message.text == "🎁 Бонусы" or message.text == "🎁":
        await message.answer("⭐️ Звезда\n💬 Напиши 'Привет'\n👑 Персона ВИП\n👤 Инкогнито\n💪🏼 НЕТ ЛИМИТУ! … Почти",
                             reply_markup=bonus_keyboard)
    elif message.text == "⭐️ Звезда" or message.text == "⭐️":
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
    elif message.text == "🏠 главное меню" or message.text == "🏠":
        user_id = message.from_user.id
        if db.is_user_registered(user_id):
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=main_keyboard)
    else:
        await message.answer("что?")


async def process_text_message(message: types.Message):
    # Handle other text messages
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('Black.json')))) != set():
        await message.reply("Мат запрещён")
        await message.delete()
    else:
        await message.answer("что?")


async def handle_create_profile(message: types.Message):
    user_id = message.from_user.id
    if db.is_user_registered(user_id):
        await message.answer("У вас уже есть анкета, хотите изменить её?", reply_markup=ReplyKeyboardRemove())
        await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=main_keyboard)
    else:
        await message.answer("Отлично! Давай начнем создание анкеты. Как тебя зовут?",
                             reply_markup=ReplyKeyboardRemove())
        await Profil.RegistrationState.name.set()


async def handle_help(message: types.Message):
    await message.answer("Выберете ваш вопрос", reply_markup=help_keyboard)


async def handle_wallet(message: types.Message):
    user_id = message.from_user.id
    wallet = db.get_user_wallet(user_id)
    if wallet is not None:
        response = f"Ваш текущий баланс: {wallet} единиц, хотите пополнить счёт?"
    else:
        response = "К сожалению, у вас нет кошелька"
    await message.answer(response)


async def handle_mutual_sympathies(message: types.Message):
    await message.answer("У тебя есть моя симпатия 😉")


def register_user(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=ContentType.TEXT)
