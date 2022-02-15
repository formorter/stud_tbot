from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

print(os.getenv('TEST_BOT_TOKEN', 'соси жопу'))
bot = Bot(token=os.getenv('TEST_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
