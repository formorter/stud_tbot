import os
import sys
import database
from utils.misc.logger import logger as log
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# print(os.getenv('TEST_BOT_TOKEN', 'соси жопу'))
token = os.getenv('MAIN_BOT_TOKEN')
for i, arg in enumerate(sys.argv):
    if arg == '-v':
        log.info('Verbose mode activated!')
    if arg == '-m' and len(sys.argv) - 1 >= i + 2:
        if os.path.isfile(sys.argv[i + 1]):
            log.info('Flag -m detected\nMigrating…')
            database.path_to_database = sys.argv[i + 2]
            database.Schedule.migrate(sys.argv[i + 1])
    if arg == '-t':
        token = os.getenv('TEST_BOT_TOKEN')
        
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
log.info('Бот загружен')
