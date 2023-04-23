from base64 import b64decode as dec64
import binascii
import sqlite3
from io import BytesIO

from PIL import Image
from aiogram.types import Message, PhotoSize

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    photo BLOB
    )
''')


def is_user_registered(user_id: int) -> bool:
    cursor.execute('SELECT COUNT(*) FROM users WHERE id = ?', (user_id,))
    count = cursor.fetchone()[0]
    return count > 0


# Создание профиля пользователя
def create_profile(user_id: int, name: str, age: int, gender: str, photo: bytes):
    cursor.execute('INSERT INTO users (id, name, age, gender, photo) VALUES (?, ?, ?, ?, ?)',
                   (user_id, name, age, gender, photo))
    conn.commit()


# Получение профиля пользователя по ID
def get_profile(user_id: int):
    cursor.execute('SELECT name, age, gender FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()


async def process_photo(message: Message):
    photo: PhotoSize = message.photo[-1]
    photo_binary = BytesIO()
    await photo.download(destination=photo_binary)
    photo_binary.seek(0)
    photo_bytes = photo_binary.read()
    cursor.execute("INSERT INTO users (photo) VALUES (?)", (photo_bytes,))
    conn.commit()


# Получение всех профилей пользователей
def get_all_profiles():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


# Удаление профиля пользователя по ID
def delete_profile(user_id: int):
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()


def get_user_photo(user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        photo_data_str = user_data[-1]
        try:
            image_bytes = dec64(photo_data_str + "=" * ((4 - len(photo_data_str) % 4) % 4))
            image = Image.open(BytesIO(image_bytes))
            return image
        except binascii.Error:
            print("Ошибка декодирования изображения")
            return None
    else:
        print("Пользователь не найден")
        return None


# Закрытие соединения с базой данных
def close_db():
    conn.close()
