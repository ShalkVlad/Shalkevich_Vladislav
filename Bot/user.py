import json
import string

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ContentType

import Profile
import DB
from Creat_Bot import bot
from User_kb import help_keyboard, main_keyboard, start_keyboard, edit_profile_keyboard, \
    edit_profile_keyboard_with_fields, bonus_keyboard


async def process_message(message: types.Message):
    commands = {
        "👋 Создать Анкету", "👋", "❓ Информация о боте", "❓", "📜 Правила сообщества", "🤔 Что я могу?",
        "💰 Кошелёк", "💰", "❤️ Взаимные симпатии", "❤️", "👀 Смотреть анкеты", "👀", "🌐 Сменить язык", "🌐",
        "😊 Моя анкета", "😊", "✏️ Изменить анкету", "✏️", "📷 Изменить фото",
        "📷", "😀 Изменить имя", "😀", "🎂 Изменить возраст", "🎂", "🌎 Изменить страну", "🌎", "✍️ Изменить описание",
        "✍️", "❌ Удалить анкету", "❌", "🆕 Новая анкета", "🆕", "🎁 Бонусы", "🎁",
        "⭐️ Звезда", "⭐️", "💬 Напиши 'Привет'", "💬", "👑 Персона ВИП", "👑", "👤‍ Инкогнито", "👤",
        "💪🏼 НЕТ ЛИМИТУ! … Почти", "💪🏼", "🏠 главное меню", "🏠"
    }

    if message.text in commands:
        await process_commands(message)
    else:
        await process_text_message(message)


async def process_commands(message: types.Message):
    text = message.text
    user_id = message.from_user.id

    if text in ["👋 Создать Анкету", "👋"]:
        if DB.is_user_registered(user_id):
            await message.answer("У вас уже есть анкета, хотите изменить её?", reply_markup=ReplyKeyboardRemove())
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=main_keyboard)
        else:
            await message.answer("Отлично! Давай начнем создание анкеты. Как тебя зовут?",
                                 reply_markup=ReplyKeyboardRemove())
            await Profile.RegistrationState.name.set()
    elif text in ["❓ Информация о боте", "❓"]:
        await message.answer("Выберете ваш вопрос", reply_markup=help_keyboard)
    elif text == ["📜 Правила сообщества", "📜"]:
        await message.answer("Значит правил в нашем боте не много):\n1.Не вздумай скидывать сюда пошлятину, "
                             "я предупредил)\n2.Будь вежлив , имей уважение к собеседнику)\n3.Нарушение правил "
                             "строго наказывается , а если точнее то вас Забанят ")
    elif text == ["🤔 Что я могу?", "🤔"]:
        await message.answer("У меня еще не много функций😔,но я могу например найти тебе пару), а возможно и "
                             "две пары, или даже три) или забанить тебя за плохое поведение! Но я надеюсь этого "
                             "не будет:) ")
    elif text in ["💰 Кошелёк", "💰"]:
        user_id = message.from_user.id
        wallet = DB.get_user_wallet(user_id)
        if wallet is not None:
            response = f"Ваш текущий баланс: {wallet} единиц, хотите пополнить счёт?"
        else:
            response = "К сожалению, у вас нет кошелька"
        await message.answer(response)
    elif text in ["❤️ Взаимные симпатии", "❤️"]:
        await message.answer("У тебя есть моя симпатия 😉")
    elif text in ["👀 Смотреть анкеты", "👀"]:
        await message.answer("В разработке")
    elif text in ["🌐 Сменить язык", "🌐"]:
        await message.answer("Ю Спык инглиш?)")
    elif text in ["🏠 главное меню", "🏠"]:
        if DB.is_user_registered(user_id):
            await message.answer("Добро пожаловать в ваш кабинет!", reply_markup=main_keyboard)
        else:
            await message.answer("Вы вернулись в главное меню", reply_markup=start_keyboard)
    elif text in ["😊 Моя анкета", "😊"]:
        profile = DB.get_profile(user_id)
        if profile:
            name, age, gender, country, about, photo, wallet = profile
            text = f"Имя: {name}\nВозраст: {age}\nПол: {gender}\nСтрана: {country}\n" \
                   f"Баллы: {wallet}\nИнформация о себе: {about}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=edit_profile_keyboard)
        else:
            text = "Профиль не найден"
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard)
    elif text in ["✏️ Изменить анкету", "✏️"]:
        await message.answer("Какие данные вы хотите изменить?", reply_markup=edit_profile_keyboard_with_fields)
    elif text in ["📷 Изменить фото", "📷"]:
        await message.answer("Хорошо! Пришлите новую фотографию для вашей анкеты:", reply_markup=ReplyKeyboardRemove())
        await Profile.Newdata.photo.set()
    elif text in ["😀 Изменить имя", "😀"]:
        await message.answer("Введите ваше новое имя:")
        await Profile.Newdata.name.set()
    elif text in ["🎂 Изменить возраст", "🎂"]:
        await message.answer("Введите ваш новый возраст (целое число):")
        await Profile.Newdata.age.set()
    elif text in ["🌎 Изменить страну", "🌎"]:
        await message.answer("Введите вашу новую страну:")
        await Profile.Newdata.country.set()
    elif text in ["✍️ Изменить описание", "✍️"]:
        await message.answer("Введите ваше новое описание:")
        await Profile.Newdata.about.set()
    elif text in ["❌ Удалить анкету", "❌"]:
        DB.delete_profile(user_id)
        await message.answer("Ваша анкета была успешно удалена.", reply_markup=start_keyboard)
    elif text in ["🆕 Новая анкета", "🆕"]:
        DB.delete_profile(user_id)
        await message.answer("Отлично! Давай начнем создание анкеты. Как тебя зовут?",
                             reply_markup=ReplyKeyboardRemove())
        await Profile.RegistrationState.name.set()
    elif text in ["🎁 Бонусы", "🎁"]:
        await message.answer("⭐️ Звезда\n💬 Напиши 'Привет'\n👑 Персона ВИП\n👤 Инкогнито\n💪🏼 НЕТ ЛИМИТУ! … Почти",
                             reply_markup=bonus_keyboard)
    elif text == "⭐️ Звезда":
        await message.answer("Наделяет тебя невероятной удачей, анкета выпадает чаще и всегда на виду стоимость 600"
                             " баллов срок 7 дней, 1100 баллов стоимость за месяц ")
    elif text == "💬 Напиши 'Привет'":
        await message.answer("Открывает для тебя не только оценить, но и написать понравившемуся пользователю "
                             "сообщение (Стоимость 800 баллов срок 7 дней, 1500 баллов за месяц)")
    elif text == "👑 Персона ВИП":
        await message.answer("Перед вами открыты все двери, всё внимание и персональный отбор анкет, для вас нет "
                             "границ. Вы персона ВИП)")
    elif text == "👤‍ Инкогнито":
        await message.answer("Вы таинственны, загадочны и можете раскрыть свою личность лишь тем, кого посчитайте"
                             " достойным")
    elif text == "💪🏼 НЕТ ЛИМИТУ! … Почти":
        await message.answer("Существующий лимит кажется слишком маленьким? Для тебя уникальное предложение "
                             "увеличь количества анкет.")
    else:
        await message.answer("что?")


async def process_text_message(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('Black.json')))) != set():
        await message.reply("Мат запрещён")
        await message.delete()
    else:
        await message.answer("что?")


def register_user(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=ContentType.TEXT)
