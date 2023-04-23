from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

btn1 = InlineKeyboardButton("👋 Создать Анкету")
btn2 = InlineKeyboardButton("❓ Информация о боте")

But_User_start = ReplyKeyboardMarkup(resize_keyboard=True)
But_User_start.add(btn1).add(btn2)

btn1 = InlineKeyboardButton("📜 Правила сообщества")
btn2 = InlineKeyboardButton("🤔 Что я могу?")
back = InlineKeyboardButton("🔙 Вернуться в главное меню")

But_User_Help = ReplyKeyboardMarkup(resize_keyboard=True)
But_User_Help.add(btn1).add(btn2).add(back)

# Кнопки для выбора темы интересов
btn1 = KeyboardButton('🎬 Кино и сериалы')
btn2 = KeyboardButton('📚 Книги и чтение')
btn3 = KeyboardButton('🍔 Еда и кулинария')
btn4 = KeyboardButton('🚴 Спорт и фитнес')
btn5 = KeyboardButton('🎮 Видеоигры')
btn6 = KeyboardButton('🎼 Музыка и концерты')
btn7 = KeyboardButton('🎨 Искусство и творчество')
btn8 = KeyboardButton('🌍 Путешествия')
btn9 = KeyboardButton('💼 Карьера и бизнес')
btn10 = KeyboardButton('👨‍👩‍👧‍👦 Семья и отношения')
btn11 = KeyboardButton('🧘 Йога и медитация')
btn12 = KeyboardButton('🐶 Животные и природа')
btn13 = KeyboardButton('🔮 Другое')

interests_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
interests_markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13)

# Кнопки для выбора возраста
age_btn1 = KeyboardButton('18-20')
age_btn2 = KeyboardButton('21-25')
age_btn3 = KeyboardButton('26-30')
age_btn4 = KeyboardButton('31-35')
age_btn5 = KeyboardButton('36-40')
age_btn6 = KeyboardButton('41-45')
age_btn7 = KeyboardButton('46-50')
age_btn8 = KeyboardButton('50+')

age_markup = InlineKeyboardMarkup(resize_keyboard=True, selective=True)
age_markup.add(age_btn1, age_btn2, age_btn3, age_btn4, age_btn5, age_btn6, age_btn7, age_btn8)

male_btn = KeyboardButton("♂️ Мужчина")
female_btn = KeyboardButton("♀️ Женщина")
other_btn = KeyboardButton("🤖 Другое")

gender_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
gender_markup.add(male_btn, female_btn, other_btn)

keyboard = ReplyKeyboardMarkup(row_width=2, selective=True, resize_keyboard=True)
btn1 = KeyboardButton(text="😊 Моя анкета")
btn2 = KeyboardButton(text="🎁 Бонусы")
btn3 = KeyboardButton(text="💰 Кошелёк")
btn4 = KeyboardButton(text="❤️ Взаимные симпатии")
btn5 = KeyboardButton(text="👀 Смотреть анкеты")
btn6 = KeyboardButton(text="🌐 Сменить язык")
keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

button_star = KeyboardButton("⭐️ Звезда")
button_hello = KeyboardButton("💬 Напиши 'Привет'")
button_vip = KeyboardButton("👑 Персона ВИП")
button_incognito = KeyboardButton("👤‍ Инкогнито")
button_limit = KeyboardButton("💪🏼 НЕТ ЛИМИТУ! … Почти")
back = InlineKeyboardButton("🏠 главное меню")


keyboard_bonus = ReplyKeyboardMarkup([[button_star, button_hello], [button_vip, button_incognito],
                                [button_limit, back]], row_width=2, selective=True, resize_keyboard=True)
