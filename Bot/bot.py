from aiogram.utils import executor
import other, user
from creat_Bot import dp


async def on_bot_start(_):
    print("Бот активен")


user.reg(dp)
other.reg_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start)
