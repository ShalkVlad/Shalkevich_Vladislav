from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from Config import TOKEN
# Инициализация бота
bot = Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
