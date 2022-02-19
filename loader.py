import os
import sys
import database
from handlers.group import event
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#print(os.getenv('TEST_BOT_TOKEN', 'соси жопу'))

for i, arg in enumerate(sys.argv):
    if arg == '-v':
        print('Verbose mode activated!')
    if arg == '-m' and len(sys.argv)-1 >= i+2:
        if os.path.isfile(sys.argv[i+1]):
            print('Flag -m detected\nMigrating…')
            database.path_to_database = sys.argv[i+2]
            database.Schedule.migrate(sys.argv[i+1])
bot = Bot(token=os.getenv('TEST_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# print(sys.argv)
print('Бот загружен')
