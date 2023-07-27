from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton

# Кнопки для клавиатур
btn_create_profile = InlineKeyboardButton("👋 Создать Анкету")
btn_bot_info = InlineKeyboardButton("❓ Информация о боте")

# Клавиатура "Начать"
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(btn_create_profile, btn_bot_info)

# Кнопки для клавиатуры "Помощь"
btn_community_rules = InlineKeyboardButton("📜 Правила сообщества")
btn_bot_capabilities = InlineKeyboardButton("🤔 Что я могу?")
btn_back_to_main_menu = InlineKeyboardButton("🏠 главное меню")

# Клавиатура "Помощь"
help_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
help_keyboard.add(btn_community_rules, btn_bot_capabilities, btn_back_to_main_menu)

# Кнопки для выбора пола
btn_male = KeyboardButton("♂️ Мужской")
btn_female = KeyboardButton("♀️ Женский")
btn_other_gender = KeyboardButton("🤖 Другое")

# Клавиатура выбора пола
gender_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
gender_markup.add(btn_male, btn_female, btn_other_gender)

# Кнопки для выбора пола партнёра
btn_other_partner_gender = KeyboardButton("🤖 Не важно")

# Клавиатура выбора пола партнёра
partner_gender_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
partner_gender_markup.add(btn_male, btn_female, btn_other_partner_gender)

# Кнопки для основной клавиатуры
btn_my_profile = KeyboardButton(text="😊 Моя анкета")
btn_bonuses = KeyboardButton(text="🎁 Бонусы")
btn_wallet = KeyboardButton(text="💰 Кошелёк")
btn_mutual_sympathies = KeyboardButton(text="❤️ Взаимные симпатии")
btn_view_profiles = KeyboardButton(text="👀 Смотреть анкеты")
btn_change_language = KeyboardButton(text="🌐 Сменить язык")

# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup(row_width=2, selective=True, resize_keyboard=True)
main_keyboard.add(btn_my_profile, btn_bonuses, btn_wallet, btn_mutual_sympathies, btn_view_profiles,
                  btn_change_language)

# Кнопки для клавиатуры "Бонусы"
btn_star_bonus = KeyboardButton("⭐️ Звезда")
btn_hello_bonus = KeyboardButton("💬 Напиши 'Привет'")
btn_vip_bonus = KeyboardButton("👑 Персона ВИП")
btn_incognito_bonus = KeyboardButton("👤‍ Инкогнито")
btn_limitless_bonus = KeyboardButton("💪🏼 НЕТ ЛИМИТУ! … Почти")

# Клавиатура "Бонусы"
bonus_keyboard = ReplyKeyboardMarkup([[btn_star_bonus, btn_hello_bonus], [btn_vip_bonus, btn_incognito_bonus],
                                      [btn_limitless_bonus, btn_back_to_main_menu]], row_width=2, selective=True,
                                     resize_keyboard=True)

# Кнопки для клавиатуры "Редактировать анкету"
btn_edit_profile = KeyboardButton("✏️ Изменить анкету")
btn_delete_profile = KeyboardButton("❌ Удалить анкету")

# Клавиатура "Редактировать анкету"
edit_profile_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
edit_profile_keyboard.add(btn_edit_profile, btn_delete_profile, btn_back_to_main_menu)

btn_edit_name = KeyboardButton("😀 Изменить имя")
btn_edit_age = KeyboardButton("🎂 Изменить возраст")
btn_edit_country = KeyboardButton("🌎 Изменить страну")
btn_edit_city = KeyboardButton("🏙️ Изменить город")
btn_edit_about = KeyboardButton("✍️ Изменить описание")
btn_change_photo = KeyboardButton("📷 Изменить фото")
btn_Nev = KeyboardButton("🆕 Новая анкета")

# Клавиатура "Редактировать анкету" с названиями полей таблицы
edit_profile_keyboard_with_fields = ReplyKeyboardMarkup(resize_keyboard=True)
edit_profile_keyboard_with_fields.add(btn_edit_name, btn_edit_age,
                                      btn_edit_country, btn_edit_city, btn_edit_about, btn_change_photo,
                                      btn_back_to_main_menu, btn_Nev)

btn_provide_location = KeyboardButton("📍 Предоставить геолокацию", request_location=True)
location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
location_keyboard.add(btn_provide_location)
