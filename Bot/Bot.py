from aiogram.utils import executor
import Other, User
from Creat_Bot import dp



async def on_bot_start(_):
    print("Бот активен")


Other.register(dp)
User.register_user(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start)
