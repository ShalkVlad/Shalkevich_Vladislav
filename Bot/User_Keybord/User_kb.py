from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

def start(texts):
    create_profile = InlineKeyboardButton(text=texts["profile"], callback_data="create_profile")
    info = InlineKeyboardButton(text=texts["info"], callback_data="info")

    starts = InlineKeyboardMarkup(row_width=2)
    starts.add(create_profile, info)

    return starts

def helps(texts):
    community = InlineKeyboardButton(text=texts["community"], callback_data="community")
    capabilities = InlineKeyboardButton(text=texts["capabi"], callback_data="capabilities")
    menu = InlineKeyboardButton(text=texts["menu"], callback_data="menu")

    helping = InlineKeyboardMarkup(row_width=2)
    helping.add(community, capabilities, menu)

    return helping

def genders(texts):
    male = KeyboardButton(text=texts["male"])
    female = KeyboardButton(text=texts["female"])
    other = KeyboardButton(text=texts["other"])

    gender = ReplyKeyboardMarkup(resize_keyboard=True)
    gender.add(male, female, other)

    return gender

def main(texts):
    buttons = [
        KeyboardButton(text=texts["MY_profile"]),
        KeyboardButton(text=texts["All_bonus"]),
        KeyboardButton(text=texts["wallets"]),
        KeyboardButton(text=texts["sympathies"]),
        KeyboardButton(text=texts["view"]),
        KeyboardButton(text=texts["language"]),
    ]
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main_menu.add(*buttons)

    return main_menu

def bonus(texts):
    buttons = [
        InlineKeyboardButton(text=texts["star"], callback_data="star"),
        InlineKeyboardButton(text=texts["hello"], callback_data="hello"),
        InlineKeyboardButton(text=texts["vip"], callback_data="vip"),
        InlineKeyboardButton(text=texts["limitless"], callback_data="limitless"),
    ]
    menu_button = InlineKeyboardButton(text=texts["menu"], callback_data="menu")
    bonuses = InlineKeyboardMarkup(row_width=2)
    bonuses.add(*buttons, menu_button)

    return bonuses

def edits(texts):
    buttons = [
        InlineKeyboardButton(text=texts["edit"], callback_data="edit"),
        InlineKeyboardButton(text=texts["delete"], callback_data="delete"),
        InlineKeyboardButton(text=texts["apply_filter"], callback_data="apply_filter"),
    ]
    menu_button = InlineKeyboardButton(text=texts["menu"], callback_data="menu")
    edit_profile_keyboard = InlineKeyboardMarkup(row_width=1)
    edit_profile_keyboard.add(*buttons, menu_button)

    return edit_profile_keyboard

def edit_prof(texts):
    buttons = [
        InlineKeyboardButton(text=texts["edit_name"], callback_data="edit_name"),
        InlineKeyboardButton(text=texts["edit_age"], callback_data="edit_age"),
        InlineKeyboardButton(text=texts["edit_country"], callback_data="edit_country"),
        InlineKeyboardButton(text=texts["edit_about"], callback_data="edit_about"),
        InlineKeyboardButton(text=texts["photo"], callback_data="photo"),
    ]
    menu_button = InlineKeyboardButton(text=texts["menu"], callback_data="menu")
    edit_profile = InlineKeyboardMarkup(row_width=1)
    edit_profile.add(*buttons, menu_button)

    return edit_profile

def cancel(texts):
    cancel_button = KeyboardButton(text=texts["Cancel"])
    cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_markup.add(cancel_button)

    return cancel_markup

def create_locations(texts):
    provide_location = KeyboardButton(text=texts["provide_location"], request_location=True)
    cancel_button = KeyboardButton(text=texts["Cancel"])

    locations = ReplyKeyboardMarkup(resize_keyboard=True)
    locations.add(provide_location, cancel_button)

    return locations

def language_keyboard():
    buttons = [
        KeyboardButton("🇷🇺 Русский"),
        KeyboardButton("🇬🇧 English"),
        KeyboardButton("🇧🇾 Беларускі"),
        KeyboardButton("🇺🇦 Українська"),
        KeyboardButton("🇵🇱 Polski"),
    ]
    language_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    language_markup.add(*buttons)

    return language_markup
