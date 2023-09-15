import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import DB
from Creat_Bot import bot, dp
from DB import get_all_profiles, session, User, Profile
from Other import load_language_texts, get_user_language
from User_kb import main, sympathies, create_nextsdelete_keyboard, \
    create_syma_keyboard, ssympathy
from likes import (add_like, get_pending_sympathy,
                   move_pending_to_mutual, get_mutually_liked_users, delete_mutual_sympathy, get_unanswered_sympathy,
                   delete_sympathy_entry, get_users_unanswered_sympathy)
from Profil_vere import get_user_preferences

btn_send_sympathy = types.KeyboardButton("❤️ Отправить симпатию")
btn_skip = types.KeyboardButton("➡️ Пропустить")
btn_back_to_main_menu = types.KeyboardButton("🏠 главное меню")

sympathy = types.ReplyKeyboardMarkup(resize_keyboard=True)
sympathy.add(btn_send_sympathy, btn_skip, btn_back_to_main_menu)


class ProfileLookupState(StatesGroup):
    show_next = State()
    respond_to_sympathy = State()


async def get_random_profiles(user_id: int, count: int):
    user_preferences = get_user_preferences(user_id)
    if not user_preferences:
        return []  # Пользовательские предпочтения отсутствуют

    all_profiles = get_all_profiles()
    unanswered_sympathy = get_users_unanswered_sympathy(user_id)
    mutually_liked_users = get_mutually_liked_users(user_id)

    filtered_profiles = [
        profile for profile in all_profiles
        if
        profile.id != user_id and profile.id not in unanswered_sympathy and profile.id not in mutually_liked_users and check_profile_against_preferences(
            profile, user_preferences)
    ]

    random.shuffle(filtered_profiles)
    return filtered_profiles[:count]


def check_profile_against_preferences(profile, preferences):
    if preferences.preferred_gender and preferences.preferred_gender != profile.gender:
        return False

    if preferences.preferred_age_min and profile.age < preferences.preferred_age_min:
        return False

    # Добавьте другие проверки, основанные на остальных предпочтениях пользователя

    return True


@dp.message_handler(state=ProfileLookupState.show_next)
async def process_profile_lookup(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    async with state.proxy() as data:
        profiles = data.get("profiles")
        current_index = data.get("current_index", 0)
        total_profiles_count = 10  # Укажите количество анкет, которое вы хотите показать

        if not profiles or current_index >= len(profiles):
            # Если анкеты закончились или это первый запуск, получаем новые анкеты
            profiles = await get_random_profiles(message.from_user.id, total_profiles_count)
            data["profiles"] = profiles
            current_index = 0

        if message.text == "❤️ Отправить симпатию":
            if current_index < len(profiles):
                # Получаем профиль пользователя, которому отправили симпатию
                liked_profile = profiles[current_index]
                recipient_id = liked_profile.id
                sender_id = message.from_user.id

                # Получаем анкету пользователя, который отправил симпатию
                sender = profil(sender_id)
                # Функция для получения данных анкеты по идентификатору из базы данных

                # Сохраняем информацию о симпатии в базе данных
                add_like(sender_id, recipient_id)

                # Переходим к следующей анкете (показываем новую анкету для оценки)
                current_index += 1
                data["current_index"] = current_index

                # Отправляем уведомление пользователю Б о том, что ему пришла симпатия от пользователя А
                if sender:
                    notification_message = (texts["Like_All"])
                    await bot.send_message(chat_id=recipient_id, text=notification_message, reply_markup=sympathies)
                    current_index += 1
                    data["current_index"] = current_index

        elif message.text == "➡️ Пропустить":
            # Пользователь решил пропустить текущую анкету,
            # переходим к следующей анкете
            current_index += 1
            data["current_index"] = current_index
        if current_index < len(profiles):
            # Показываем текущую анкету
            profile = profiles[current_index]
            await show_profile_with_sympathy_keyboard(message, profile)
        else:
            await state.finish()
            await message.answer(texts["welcome_message"], reply_markup=main(texts))


async def show_profile_with_sympathy_keyboard(message: types.Message, profile):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    name = profile.name
    age = profile.age
    gender = profile.gender
    country = profile.country
    about = profile.about
    photo = profile.photo  # Здесь получаем ссылку на фотографию профиля
    city = profile.city

    text = (
        f"{name}, {age}, {texts['gender']}, {gender}\n {texts['country']}: {country}, {city}\n"
        f"{texts['ABout']}: {about}")
    # Отправляем фотографию как объект File, а не ссылку на фотографию
    if photo:
        await message.answer_photo(photo=photo, caption=text, reply_markup=sympathy)
    else:
        await message.answer(text, reply_markup=create_syma_keyboard(texts))


def profil(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return Profile(
            name=user.name,
            age=user.age,
            gender=user.gender,
            country=user.country,
            about=user.about,
            photo=user.photo,
            wallet=user.wallet,
            city=user.city,
            telegram_username=user.telegram_username
        )
    else:
        return None


@dp.message_handler(lambda message: message.text == "😍 Показать симпатии", state="*")
async def show_sympathy_message(message: types.Message, state: FSMContext):
    user = message.from_user.id
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    # Получаем список пользователей, на которых текущий пользователь отправил симпатию,
    # но не получил взаимного лайка
    pending_sympathy_users = get_pending_sympathy(user)

    if not pending_sympathy_users:
        await message.answer(texts["MYSIMP"])
        return

    async with state.proxy() as data:
        current_index = data.get("current_index", 0)

        if current_index >= len(pending_sympathy_users):
            # Если все анкеты были просмотрены, сбрасываем индекс обратно на 0
            current_index = 0

        # Выбираем пользователя из списка по текущему индексу
        recipient_id = pending_sympathy_users[current_index]

        # Получаем профиль пользователя, который отправил симпатию
        recipient_profile = profil(recipient_id)

        if recipient_profile:
            # Формируем текст уведомления с информацией из профиля пользователя, который отправил симпатию
            notification_message = f"{recipient_profile.name}, {recipient_profile.age}, " \
                                   f"{texts['gender']}, {recipient_profile.gender}\n" \
                                   f"{texts['country']}, {recipient_profile.country}, {recipient_profile.city}\n" \
                                   f"{texts['ABout']}, {recipient_profile.about}"

            # Отправляем фотографию и уведомление пользователю
            await bot.send_photo(chat_id=user, photo=recipient_profile.photo,
                                 caption=notification_message, reply_markup=create_syma_keyboard(texts))

            # Обновляем индекс анкеты в данных состояния
            current_index += 1
            data["current_index"] = current_index
            await state.update_data(data)  # Обновляем данные в состоянии
            return

        else:
            # Если не удалось получить профиль пользователя, просто пропускаем эту анкету
            current_index += 1
            data["current_index"] = current_index
            await state.set_data(data)
            return


@dp.message_handler(lambda message: message.text == "🚀 Следующая", state=ProfileLookupState.show_next)
async def skip_sympathy_message(message: types.Message, state: FSMContext):
    await show_sympathy_message(message, state)


@dp.message_handler(lambda message: message.text == "♥️ Ответить взаимностью", state="*")
async def process_mutual_sympathy(message: types.Message, state: FSMContext):
    user = message.from_user.id
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    # Получаем список пользователей, на которых текущий пользователь отправил симпатию,
    # но не получил взаимного лайка
    pending_sympathy_users = get_pending_sympathy(user)

    if not pending_sympathy_users:
        await message.answer(texts["MYSIMP"], reply_markup=ssympathy(texts))
        await ProfileLookupState.show_next.set()  # Переводим пользователя в состояние просмотра анкет
        return

    # Получаем данные из состояния пользователя
    data = await state.get_data()
    current_index = data.get("current_index", 0) - 1

    # Если пользователь ответил на все симпатии, сбрасываем индекс обратно на 0
    if current_index >= len(pending_sympathy_users):
        current_index = 0

    # Выбираем пользователя из списка по текущему индексу
    recipient_id = pending_sympathy_users[current_index]

    # Получаем профиль отправителя симпатии (текущий пользователь)
    sender_profile = profil(user)
    # Получаем профиль получателя симпатии
    recipient_profile = profil(recipient_id)

    # Если профили отправителя и получателя успешно получены, продолжаем
    if sender_profile and recipient_profile:
        # Удаляем информацию о не взаимной симпатии и перемещаем взаимные симпатии
        move_pending_to_mutual(user)
        move_pending_to_mutual(recipient_id)

        sender_name_link = f"<a href='https://t.me/{sender_profile.telegram_username}'>{sender_profile.name}</a>"
        recipient_name_link = f"<a href='https://t.me/{recipient_profile.telegram_username}'>{recipient_profile.name}</a>"

        # Уведомляем об отправителе взаимной симпатии
        notification_message_sender = f"{texts['LAVE']},{recipient_name_link}"
        # Уведомляем получателя о взаимной симпатии
        notification_message_recipient = f"{texts['LIKEME']},{sender_profile.name}, {sender_profile.age}, " \
                                         f"{texts['gender']} {sender_profile.gender}\n" \
                                         f"{texts['country']}: {sender_profile.country}, {sender_profile.city}\n" \
                                         f"{texts['ABout']} {sender_profile.about}\n" \
                                         f"{texts['MESME']} {sender_name_link}"

        # Отправляем фотографии и уведомления обоим пользователям
        await bot.send_message(chat_id=user, text=notification_message_sender, parse_mode='HTML', reply_markup=main)

        await bot.send_photo(chat_id=recipient_id, photo=sender_profile.photo,
                             caption=notification_message_recipient,
                             reply_markup=main, parse_mode='HTML')
        # Обновляем индекс анкеты в данных состояния
        current_index += 1
        data["current_index"] = current_index
        await state.update_data(data)  # Обновляем данные в состоянии

    else:
        # Если профили не были успешно получены, просто пропускаем эту анкету
        current_index += 1
        data["current_index"] = current_index
        await state.set_data(data)  # Обновляем данные в состоянии
    return


@dp.message_handler(lambda message: message.text == "💞 Ваши взаимные симпатии", state="*")
async def sympathy_profiles(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    mutual_sympathy_list = get_mutually_liked_users(user_id)

    if mutual_sympathy_list:
        data = await state.get_data()
        current_profile_index = data.get("current_profile_index", 0)

        if current_profile_index < len(mutual_sympathy_list):
            profile_user_id = mutual_sympathy_list[current_profile_index]
            profile = profil(profile_user_id)

            if profile:
                recipient_name_link = f"<a href='https://t.me/{profile.telegram_username}'>{profile.name}</a>"
                reply_message = (
                    f"{profile.name}, {profile.age}, {texts['gender']}, {profile.gender}\n",
                    f"{texts['country']}: {profile.country}, {profile.city}\n, "
                    f"{texts['ABout']}:{profile.about}\n"
                    f"{texts['Message']}:{recipient_name_link}"
                )

                if profile.photo:
                    await message.answer_photo(
                        photo=profile.photo, caption=reply_message, parse_mode='HTML',
                        reply_markup=create_nextsdelete_keyboard(texts))
                else:
                    await message.answer(reply_message, parse_mode='HTML')

                new_index = current_profile_index + 1
                if new_index >= len(mutual_sympathy_list):
                    new_index = 0  # Если индекс больше или равен количеству анкет, вернуть индекс к 0

                # Обновляем индекс анкеты в данных состояния
                data["current_profile_index"] = new_index
                await state.update_data(data)
            else:
                await message.answer(texts['NO_ANKET'])
        else:
            await message.answer(texts['NO_SIMP'], reply_markup=ssympathy(texts))
    else:
        await message.answer(texts['NO_DATA'], reply_markup=ssympathy(texts))


@dp.message_handler(lambda message: message.text == "⏭ Следующая", state="*")
async def callback_show_next_profile(message: types.Message, state: FSMContext):
    await sympathy_profiles(message, state)


@dp.message_handler(lambda message: message.text == "💝 Вы отправили симпатию", state="*")
async def show_sent_sympathy_profiles(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    # Получить список пользователей, которым отправили симпатию текущий пользователь
    users_sent_sympathy = get_unanswered_sympathy(user_id)

    if users_sent_sympathy:
        profiles = [profil(user_id) for user_id in users_sent_sympathy]

        data = await state.get_data()
        current_profile_index = data.get("current_profile_index", 0) - 1

        if current_profile_index < len(profiles):
            profile = profiles[current_profile_index]

            if profile:
                reply_message = (f"{profile.name}, {profile.age}, {texts['gender']}, {profile.gender}\n",
                                 f"{texts['country']}, {profile.country}, {profile.city}\n, "
                                 f"{texts['ABout']}, {profile.about}\n")
                if profile.photo:
                    await message.answer_photo(photo=profile.photo, caption=reply_message,
                                               parse_mode='HTML', reply_markup=create_nextsdelete_keyboard(texts))
                else:
                    await message.answer(reply_message, parse_mode='HTML')

                new_index = current_profile_index + 1
                if new_index >= len(profiles):
                    new_index = 0  # Если индекс больше или равен количеству анкет, вернуть индекс к 0
                await state.update_data(current_profile_index=new_index)
        else:
            await message.answer(texts["SERCH"], reply_markup=ssympathy(texts))

    else:
        await message.answer(texts["NO_SERCH"], reply_markup=ssympathy(texts))


@dp.message_handler(lambda message: message.text == "❌ Удалить", state="*")
async def delete_sympathy(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    user_id = message.from_user.id

    # Получаем список пользователей с взаимными симпатиями
    mutual_sympathy_list = get_mutually_liked_users(user_id)

    data = await state.get_data()
    current_profile_index = data.get("current_profile_index", 0) - 1

    if current_profile_index < len(mutual_sympathy_list):
        other_user_id = mutual_sympathy_list[current_profile_index]
        delete_mutual_sympathy(user_id, other_user_id)

        # Обновляем данные состояния
        await state.update_data(current_profile_index=current_profile_index)

        # Показываем следующую анкету
        await sympathy_profiles(message, state)

    else:
        await message.answer(texts["Sympa_Del"])


@dp.message_handler(lambda message: message.text == "▶️ Следующая", state="*")
async def nextsprofile(message: types.Message, state: FSMContext):
    await show_sent_sympathy_profiles(message, state)


@dp.message_handler(lambda message: message.text == "✖️ Удалить", state="*")
async def delete_unanswered_sympathy(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    user_id = message.from_user.id

    # Получаем список пользователей, которым отправили симпатию текущий пользователь
    unanswered_sympathy_list = get_unanswered_sympathy(user_id)

    data = await state.get_data()
    current_profile_index = data.get("current_profile_index", 0) - 1

    if current_profile_index < len(unanswered_sympathy_list):
        other_user_id = unanswered_sympathy_list[current_profile_index]
        delete_sympathy_entry(user_id, other_user_id)

        # Обновляем данные состояния
        await state.update_data(current_profile_index=current_profile_index)

        # Показываем следующую анкету
        await show_sent_sympathy_profiles(message, state)

    else:
        await message.answer(texts["No_sympa"])
