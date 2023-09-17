import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import DB
from Creat_Bot import bot, dp
from DB import get_all_profiles, session, User, Profile
from Other import load_language_texts, get_user_language
from User_kb import main, sympathies, create_nextsdelete_keyboard, \
    create_syma_keyboard, ssympathy, create_sympathy
from likes import (add_like, get_pending_sympathy,
                   move_pending_to_mutual, get_mutually_liked_users, delete_mutual_sympathy, get_unanswered_sympathy,
                   delete_sympathy_entry, get_users_unanswered_sympathy)
from Profil_vere import get_user_preferences


# Определение состояния для поиска анкет
class ProfileLookupState(StatesGroup):
    show_next = State()
    respond_to_sympathy = State()


# Функция для получения случайных анкет, удовлетворяющих предпочтениям пользователя
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


# Функция для проверки анкеты на соответствие предпочтениям пользователя
def check_profile_against_preferences(profile, preferences):
    if preferences.preferred_gender and preferences.preferred_gender != profile.gender:
        return False

    if preferences.preferred_age_min and profile.age < preferences.preferred_age_min:
        return False

    # Добавьте другие проверки, основанные на остальных предпочтениях пользователя

    return True


# Обработчик сообщений в состоянии show_next
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

        if message.text == (texts["add_simpaty"]):
            if current_index < len(profiles):
                liked_profile = profiles[current_index]
                recipient_id = liked_profile.id
                sender_id = message.from_user.id
                sender = profil(sender_id)

                add_like(sender_id, recipient_id)

                current_index += 1
                data["current_index"] = current_index

                if sender:
                    notification_message = (texts["Like_All"])
                    await bot.send_message(chat_id=recipient_id, text=notification_message, reply_markup=sympathies)
                    current_index += 1
                    data["current_index"] = current_index

        elif message.text == (texts["Nexts"]):
            current_index += 1
            data["current_index"] = current_index
        elif message.text == (texts["menu"]):
            await state.finish()
            await message.answer(texts["welcome_message"], reply_markup=main(texts))
            return

        if current_index < len(profiles):
            profile = profiles[current_index]
            await show_profile_with_sympathy_keyboard(message, profile)
        else:
            await state.finish()
            await message.answer(texts["welcome_message"], reply_markup=main(texts))


# Функция для отображения анкеты с клавиатурой симпатии
async def show_profile_with_sympathy_keyboard(message: types.Message, profile):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))

    name = profile.name
    age = profile.age
    gender = profile.gender
    country = profile.country
    about = profile.about
    photo = profile.photo
    city = profile.city

    text = (
        f"{name}, {age}, {texts['gender']}, {gender}\n {texts['country']}: {country}, {city}\n"
        f"{texts['ABout']}: {about}")

    if photo:
        await message.answer_photo(photo=photo, caption=text, reply_markup=create_sympathy(texts))
    else:
        await message.answer(text, reply_markup=create_syma_keyboard(texts))


# Функция для получения данных анкеты по идентификатору пользователя из базы данных
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


# Обработчик сообщений для отображения взаимных симпатий
async def show_sympathy_message(message: types.Message, state: FSMContext):
    user = message.from_user.id
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    pending_sympathy_users = get_pending_sympathy(user)

    if not pending_sympathy_users:
        await message.answer(texts["MY_SIMP"])
        return

    async with state.proxy() as data:
        current_index = data.get("current_index", 0)

        if current_index >= len(pending_sympathy_users):
            current_index = 0

        recipient_id = pending_sympathy_users[current_index]
        recipient_profile = profil(recipient_id)

        if recipient_profile:
            recipient_name_link = f"<a href='https://t.me/{recipient_profile.telegram_username}'>{recipient_profile.name}</a>"
            notification_message = f"{texts['LAVE']},{recipient_name_link}"

            await bot.send_photo(chat_id=user, photo=recipient_profile.photo,
                                 caption=notification_message, reply_markup=main)

            await bot.send_message(chat_id=recipient_id, text=notification_message, reply_markup=main)
            current_index += 1
            data["current_index"] = current_index
            await state.update_data(data)
            return

        else:
            current_index += 1
            data["current_index"] = current_index
            await state.set_data(data)
            return


# Обработчик сообщений для пропуска взаимных симпатий
async def skip_sympathy_message(message: types.Message, state: FSMContext):
    await show_sympathy_message(message, state)


# Обработчик сообщений для обработки взаимных симпатий
async def process_mutual_sympathy(message, state):
    user = message.from_user.id
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    pending_sympathy_users = get_pending_sympathy(user)

    if not pending_sympathy_users:
        await message.answer(texts["MY_SIMP"], reply_markup=ssympathy(texts))
        await ProfileLookupState.show_next.set()
        return

    data = await state.get_data()
    current_index = data.get("current_index", 0) - 1

    if current_index >= len(pending_sympathy_users):
        current_index = 0

    recipient_id = pending_sympathy_users[current_index]
    sender_profile = profil(user)
    recipient_profile = profil(recipient_id)

    if sender_profile and recipient_profile:
        move_pending_to_mutual(user)
        move_pending_to_mutual(recipient_id)

        sender_name_link = f"<a href='https://t.me/{sender_profile.telegram_username}'>{sender_profile.name}</a>"
        recipient_name_link = f"<a href='https://t.me/{recipient_profile.telegram_username}'>{recipient_profile.name}</a>"

        notification_message_sender = f"{texts['LAVE']},{recipient_name_link}"
        notification_message_recipient = f"{texts['LIKEME']},{sender_profile.name}, {sender_profile.age}, " \
                                         f"{texts['gender']} {sender_profile.gender}\n" \
                                         f"{texts['country']}: {sender_profile.country}, {sender_profile.city}\n" \
                                         f"{texts['ABout']} {sender_profile.about}\n" \
                                         f"{texts['MESME']} {sender_name_link}"

        await bot.send_message(chat_id=user, text=notification_message_sender, parse_mode='HTML', reply_markup=main)

        await bot.send_photo(chat_id=recipient_id, photo=sender_profile.photo,
                             caption=notification_message_recipient,
                             reply_markup=main, parse_mode='HTML')

        current_index += 1
        data["current_index"] = current_index
        await state.update_data(data)

    else:
        current_index += 1
        data["current_index"] = current_index
        await state.set_data(data)
    return


# Обработчик сообщений для просмотра отправленных симпатий
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
                    f"{profile.name}, {profile.age}, {texts['gender']}, {profile.gender}\n"
                    f"{texts['country']}, {profile.country}, {profile.city}\n"
                    f"{texts['ABout']}, {profile.about}\n,{recipient_name_link}")
                if profile.photo:
                    await message.answer_photo(
                        photo=profile.photo, caption=reply_message, parse_mode='HTML',
                        reply_markup=create_nextsdelete_keyboard(texts))
                else:
                    await message.answer(reply_message, parse_mode='HTML')

                new_index = current_profile_index + 1
                if new_index >= len(mutual_sympathy_list):
                    new_index = 0

                data["current_profile_index"] = new_index
                await state.update_data(data)
        else:
            await message.answer(texts["SERCH"], reply_markup=ssympathy(texts))

    else:
        await message.answer(texts["NO_DATA"], reply_markup=ssympathy(texts))


# Обработчик сообщений для перехода к следующей анкете отправленных симпатий
async def callback_show_next_profile(message: types.Message, state: FSMContext):
    await sympathy_profiles(message, state)


# Обработчик сообщений для удаления взаимных симпатий
async def delete_sympathy(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    user_id = message.from_user.id
    mutual_sympathy_list = get_mutually_liked_users(user_id)

    data = await state.get_data()
    current_profile_index = data.get("current_profile_index", 0) - 1

    if current_profile_index < len(mutual_sympathy_list):
        other_user_id = mutual_sympathy_list[current_profile_index]
        delete_mutual_sympathy(user_id, other_user_id)
        await state.update_data(current_profile_index=current_profile_index)
        await sympathy_profiles(message, state)
    else:
        await message.answer(texts["Sympa_Del"])


# Обработчик сообщений для отображения отправленных симпатий
async def show_sent_sympathy_profiles(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    users_sent_sympathy = get_unanswered_sympathy(user_id)

    if users_sent_sympathy:
        profiles = [profil(user_id) for user_id in users_sent_sympathy]
        data = await state.get_data()
        current_profile_index = data.get("current_profile_index", 0) - 1

        if current_profile_index < len(profiles):
            profile = profiles[current_profile_index]

            if profile:
                reply_message = (
                    f"{profile.name}, {profile.age}, {texts['gender']}, {profile.gender}\n"
                    f"{texts['country']}, {profile.country}, {profile.city}\n"
                    f"{texts['ABout']}, {profile.about}\n")
                if profile.photo:
                    await message.answer_photo(photo=profile.photo, caption=reply_message,
                                               parse_mode='HTML', reply_markup=create_nextsdelete_keyboard(texts))
                else:
                    await message.answer(reply_message, parse_mode='HTML')

                new_index = current_profile_index + 1
                if new_index >= len(profiles):
                    new_index = 0

                await state.update_data(current_profile_index=new_index)
        else:
            await message.answer(texts["SERCH"], reply_markup=ssympathy(texts))

    else:
        await message.answer(texts["NO_SEARCH"], reply_markup=ssympathy(texts))


# Обработчик сообщений для пропуска отправленных симпатий
async def nextsprofile(message: types.Message, state: FSMContext):
    await show_sent_sympathy_profiles(message, state)


# Обработчик сообщений для удаления неотвеченных симпатий
async def delete_unanswered_sympathy(message: types.Message, state: FSMContext):
    texts = load_language_texts(get_user_language(message.from_user.id, DB.session))
    user_id = message.from_user.id
    unanswered_sympathy_list = get_unanswered_sympathy(user_id)

    data = await state.get_data()
    current_profile_index = data.get("current_profile_index", 0) - 1

    if current_profile_index < len(unanswered_sympathy_list):
        other_user_id = unanswered_sympathy_list[current_profile_index]
        delete_sympathy_entry(user_id, other_user_id)
        await state.update_data(current_profile_index=current_profile_index)
        await show_sent_sympathy_profiles(message, state)
    else:
        await message.answer(texts["No_sympa"])
