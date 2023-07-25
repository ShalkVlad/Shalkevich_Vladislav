from aiogram.utils import executor
import Other, User
from Creat_Bot import dp


# Функция, которая вызывается при старте бота
async def on_bot_start(_):
    print("Бот активен")


# Регистрация обработчиков команд и текстовых сообщений из файлов "other.py" и "user.py"
Other.register(dp)
User.register_user(dp)

if __name__ == '__main__':
    # Запуск бота с обработкой команд и текстовых сообщений
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start)
