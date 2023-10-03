import json
import random
import string

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from DataBase import DB, Profil_vere
from Language.Language import (belarusian_language, ukrainian_language, english_language, polish_language,
                               russian_language, Language, get_user_texts)
from Seting.Creat_Bot import bot
from Seting.Other import command_start
from User import Profile, preper, search
from User_Keybord.User_kb import Create, start, main, edits, edit_prof, cancel, genders, update_preferences, bonus, \
    sympathy, create_locations, location


async def create_profile(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["create_profile"])


async def about_bot(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["about_bot"])


async def start_profile_creation(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["create_profile"], reply_markup=Create(texts))
    await Profile.RegistrationState.name.set()


async def process_fallback_response(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    fallback_responses = texts.get("fallback_responses", {})
    responses = random.choice(list(fallback_responses.values()))
    await message.answer(responses)


async def community_rules(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["community_rules"])


async def what_can_i_do(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["what_can_i_do"])


async def main_menu(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    user_id = message.from_user.id
    user = DB.get_user(user_id)
    if not user.photo:
        await message.answer(texts["main_menu"], reply_markup=start(texts))
    else:
        await message.answer(texts["welcome_message"], reply_markup=main(texts))


async def wallet(message: types.Message):
    user_id = message.from_user.id
    user_wallet = DB.get_user_wallet(user_id)
    texts = get_user_texts(message.from_user.id, DB.session)
    responses = f"{texts['current_balance']}: {user_wallet} {texts['currency']}, {texts['top_up_balance']}"
    await message.answer(responses)


async def update_telegram_username(user_id: int, new_username: str):
    user = DB.get_user(user_id)
    if user:
        if user.telegram_username != new_username:
            user.telegram_username = new_username
            DB.session.commit()
            return True
    return False


async def my_profile(message: types.Message):
    user_id = message.from_user.id
    profile = DB.get_profile(user_id)
    if profile:
        name, age, gender, country, about, photo, user_wallet, city = profile
        texts = get_user_texts(message.from_user.id, DB.session)
        text = (
            f"{name}, {age}, {texts['gender']} {gender}\n"
            f"{texts['country']} {country}, {texts['city']} {city}\n"
            f"{texts['YOU_wallet']} {user_wallet}\n{texts['about']} {about}"
        )
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text,
                             reply_markup=edits(texts))


async def edit_profile(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["edit_profile"], reply_markup=edit_prof(texts))


async def change_photo(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_photo"], reply_markup=cancel(texts))
    await Profile.RegistrationState.photo.set()


async def change_name(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_name"], reply_markup=cancel(texts))
    await Profile.RegistrationState.name.set()


async def change_age(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_age"], reply_markup=cancel(texts))
    await Profile.RegistrationState.age.set()


async def change_country(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_country"], reply_markup=location(texts))
    await Profile.RegistrationState.country.set()


async def change_preferred_age(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_preferred_age"], reply_markup=cancel(texts))
    await preper.ProfileState.preferred_age.set()


async def change_description(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_description"], reply_markup=cancel(texts))
    await Profile.RegistrationState.about.set()


async def change_search_country(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_search_country"], reply_markup=create_locations(texts))
    await preper.ProfileState.preferred_country.set()


async def identity_verification(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["identity_verification"], reply_markup=cancel(texts))


async def change_preferred_gender(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["change_preferred_gender"], reply_markup=genders(texts))
    await preper.ProfileState.preferred_gender.set()


async def filter_profiles(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["filter_profiles"], reply_markup=update_preferences(texts))


async def delete_profile(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    user_id = message.from_user.id
    DB.delete_user_profile(user_id)
    await message.answer(texts["delete_profile"], reply_markup=start(texts))
    await command_start(message)


async def bonuses(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["bonus"], reply_markup=bonus(texts))


async def star_bonus(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["star_bonus"])


async def say_hello_bonus(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["say_hello_bonus"])


async def vip_person_bonus(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["vip_person_bonus"])


async def no_limits_bonus(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["no_limits_bonus"])


async def process_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_username = message.from_user.username
    await update_telegram_username(user_id, new_username)
    texts = get_user_texts(message.from_user.id, DB.session)
    text = message.text

    user = DB.get_user(user_id)
    if user and not user.photo:
        commands_dict = texts.get("Allowed_commands", {})
        state_commands = {}  # Инициализируем пустым словарем
    else:
        commands_dict = texts.get("commands", {})
        state_commands = texts.get("States", {})

    if text in commands_dict:
        command_function_name = commands_dict[text]
        command_function = globals().get(command_function_name)
        if command_function:
            await command_function(message)
            return
        else:
            await process_fallback_response(message)
            return
    if text in state_commands:
        command_function_name = state_commands[text]
        command_function = globals().get(command_function_name)
        if command_function:
            await command_function(message, state)
        else:
            await process_fallback_response(message)
    else:
        await process_fallback_response(message)

    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in text.split(' ')} \
            .intersection(set(json.load(open('Language/Black.json')))) != set():
        await message.reply("Мат запрещён")
        await message.delete()


async def sympty(message: types.Message):
    texts = get_user_texts(message.from_user.id, DB.session)
    await message.answer(texts["symptom"], reply_markup=sympathy(texts))


async def start_profile_lookup(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    texts = get_user_texts(message.from_user.id, DB.session)
    preferences = Profil_vere.get_user_preferences(user_id)
    if not preferences:
        await message.reply(texts["age_range_prompt"], reply_markup=Create(texts))
        await preper.ProfileState.preferred_age.set()
        return
    else:
        await search.ProfileLookupState.show_next.set()
        await search.process_profile_lookup(message, state)


async def show_sympathy_command(message: types.Message, state: FSMContext):
    await search.show_sympathy_message(message, state)


async def show_received_sympathy(message: types.Message, state: FSMContext):
    await search.show_sent_sympathy_profiles(message, state)


async def show_mutual_sympathy_profiles(message: types.Message, state: FSMContext):
    await search.sympathy_profiles(message, state)


async def show_sympathy(message: types.Message, state: FSMContext):
    await search.skip_sympathy_message(message, state)


async def received_sympathy(message: types.Message, state: FSMContext):
    await search.process_mutual_sympathy(message, state)


async def Next_add(message: types.Message, state: FSMContext):
    await search.nextsprofile(message, state)


async def Next(message: types.Message, state: FSMContext):
    await search.callback_show_next_profile(message, state)


async def Delte(message: types.Message, state: FSMContext):
    await search.delete_unanswered_sympathy(message, state)


async def Delte_Add(message: types.Message, state: FSMContext):
    await search.delete_sympathy(message, state)


def register_user(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=ContentType.TEXT)
