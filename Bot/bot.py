from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.executor import Executor

from Setting import Other
from Setting.Creat_Bot import bot_token
from User import User_Main

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Register handlers
Other.register(router)
User_Main.register_user(router)

dp.include_router(router)

async def on_startup(dispatcher: Dispatcher):
    print("Bot is active")

    # Set bot commands (optional)
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help")
    ]
    await bot.set_my_commands(commands)

if __name__ == "__main__":
    executor = Executor(dispatcher=dp, skip_updates=True, on_startup=on_startup)
    executor.run_polling(bot)
