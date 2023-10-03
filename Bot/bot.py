from aiogram.utils import executor

from Seting import Other
from Seting.Creat_Bot import dp
from User import User_Main


async def on_bot_start(_):
    print("Бот активен")


Other.register(dp)
User_Main.register_user(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start)
