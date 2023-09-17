from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton


def start(texts):
    create_profile = InlineKeyboardButton((texts["profile"]))
    info = InlineKeyboardButton((texts["info"]))

    # Клавиатура "Начать"
    starts = ReplyKeyboardMarkup(resize_keyboard=True)
    starts.add(create_profile, info)

    return starts


def helps(texts):
    community = InlineKeyboardButton((texts["community"]))
    capabilities = InlineKeyboardButton((texts["capabi"]))
    Mein_Menu = InlineKeyboardButton((texts["menu"]))

    helping = ReplyKeyboardMarkup(resize_keyboard=True)
    helping.add(community, capabilities, Mein_Menu)

    return helping


def genders(texts):
    male = KeyboardButton(texts["male"])
    female = KeyboardButton(texts["female"])
    other = KeyboardButton(texts["other"])

    gender = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    gender.add(male, female, other)

    return gender


def main(texts):
    MY_profile = KeyboardButton(texts["MY_profile"])
    Bonus = KeyboardButton(texts["bonus"])
    wallet = KeyboardButton(texts["wallets"])
    Sympathies = KeyboardButton(texts["sympathies"])
    view = KeyboardButton(texts["view"])
    Language = KeyboardButton(texts["language"])

    Main = ReplyKeyboardMarkup(row_width=2, selective=True, resize_keyboard=True)
    Main.add(MY_profile, Bonus, wallet, Sympathies, view, Language)

    return Main


def bonus(texts):
    star = KeyboardButton(texts["star"])
    hello = KeyboardButton(texts["hello"])
    vip = KeyboardButton(texts["vip"])
    incognito = KeyboardButton(texts["incognito"])
    limitless = KeyboardButton(texts["limitless"])
    men = InlineKeyboardButton(texts["menu"])

    bonuses = ReplyKeyboardMarkup([[star, hello], [vip, incognito],
                                   [limitless, men]], row_width=2, selective=True,
                                  resize_keyboard=True)
    return bonuses


def edits(texts):
    edit = KeyboardButton(texts["edit"])
    delete = KeyboardButton(texts["delete"])
    apply_filter = KeyboardButton(texts["apply_filter"])
    menU = InlineKeyboardButton(texts["menu"])

    edit_profile_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    edit_profile_keyboard.add(edit, delete, menU, apply_filter)
    return edit_profile_keyboard


def edit_prof(texts):
    edit_name = KeyboardButton(texts["edit_name"])
    edit_age = KeyboardButton(texts["edit_age"])
    edit_country = KeyboardButton(texts["edit_country"])
    edit_city = KeyboardButton(texts["edit_city"])
    edit_about = KeyboardButton(texts["edit_about"])
    photo = KeyboardButton(texts["photo"])
    me = InlineKeyboardButton(texts["menu"])

    EditS = ReplyKeyboardMarkup(resize_keyboard=True)
    EditS.add(edit_name, edit_age,
              edit_country, edit_city, edit_about, photo,
              me)
    return EditS


def cancel(texts):
    cancelS = KeyboardButton(texts["Cancel"])
    cancelel = ReplyKeyboardMarkup(resize_keyboard=True)
    cancelel.add(cancelS)
    return cancelel


def create_locations_keyboard(texts):
    provide_location = KeyboardButton(texts["provide_location"], request_location=True)
    cancelS = KeyboardButton(texts["Cancel"])
    locations = ReplyKeyboardMarkup(selective=True, resize_keyboard=True)
    locations.add(provide_location, cancelS)
    return locations


def ssympathy(texts):
    send_sympathy = KeyboardButton(texts["send_sympathy"])
    received_sympathy = KeyboardButton(texts["received_sympathy"])
    mutual_sympathy = KeyboardButton(texts["mutual_sympathy"])
    Menu = InlineKeyboardButton(texts["menu"])

    Ssympathy = ReplyKeyboardMarkup(resize_keyboard=True)
    Ssympathy.add(mutual_sympathy, received_sympathy, send_sympathy, Menu)

    return Ssympathy


def sympathies(texts):
    sympathiesS = KeyboardButton(texts["sympathies"])

    sympathi = ReplyKeyboardMarkup(selective=True, resize_keyboard=True)
    sympathi.add(sympathiesS)

    return sympathi


def create_syma_keyboard(texts):
    skip = KeyboardButton(texts["skip"])
    sympathyS = KeyboardButton(texts["sympathyS"])
    menuu = InlineKeyboardButton(texts["menu"])

    syma = ReplyKeyboardMarkup(resize_keyboard=True)
    syma.add(sympathyS, skip, menuu)

    return syma


def create_nextsdelete_keyboard(texts):
    Nexts = KeyboardButton(texts["Nexts"])
    Deletes = KeyboardButton(texts["Deletes"])
    litl_menu = InlineKeyboardButton(texts["menu"])

    nextsdelete = ReplyKeyboardMarkup(resize_keyboard=True)
    nextsdelete.add(Nexts, Deletes, litl_menu)

    return nextsdelete


def update_preferences(texts):
    update_age = KeyboardButton(texts["update_age"])
    update_city = KeyboardButton(texts["update_city"])
    update_country = KeyboardButton(texts["update_country"])
    update_confirmation = KeyboardButton(texts["update_confirmation"])
    gena = KeyboardButton(texts["gena"])
    MYmenu = InlineKeyboardButton(texts["menu"])

    update_preferences_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    update_preferences_keyboard.add(update_age, update_city, update_country, update_confirmation, gena, MYmenu)

    return update_preferences_keyboard


def Create(texts):
    Cancels = KeyboardButton(texts["cancelS"])

    Cancel = ReplyKeyboardMarkup(resize_keyboard=True)
    Cancel.add(Cancels)

    return Cancel


def location(texts):
    Location = KeyboardButton(texts["location"], request_location=True)
    Cancel = KeyboardButton(texts["cancelS"])

    locations = ReplyKeyboardMarkup(selective=True, resize_keyboard=True)
    locations.add(Location, Cancel)

    return locations


def create_sympathy(texts):
    sympathys = KeyboardButton(texts["add_simpaty"])
    skip = KeyboardButton(texts["Nexts"])
    back = KeyboardButton(texts["menu"])

    sympathy = ReplyKeyboardMarkup(resize_keyboard=True)
    sympathy.add(sympathys, skip, back)

    return sympathy


russian_language = KeyboardButton("🇷🇺 Русский")
english_language = KeyboardButton("🇬🇧 English")
belarusian_language = KeyboardButton("🇧🇾 Беларускі")
ukrainian_language = KeyboardButton("🇺🇦 Українська")
polish_language = KeyboardButton("🇵🇱 Polski")
menu = KeyboardButton("/start")

language = ReplyKeyboardMarkup(resize_keyboard=True)
language.add(russian_language, english_language, belarusian_language, ukrainian_language, polish_language, menu)
