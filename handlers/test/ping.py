from aiogram import types
from database import Schedule
from datetime import datetime
from loader import dp, bot
from utils.misc.logger import logger as log
from handlers.group.event import is_upper_week, chat_ids

@dp.message_handler(commands=['ping'])
async def ping_command(message: types.Message):
    await bot.send_message(message.chat.id, 'pong!')
    log.info('Pong command from {}'.format(message.from_user.username))


@dp.message_handler(commands=['schedule'])
async def schedule_command(message: types.Message):
    day = datetime.strftime(datetime.now(), '%A')
    sep = '\n' + '-' * 20 + '\n'
    schedule = []
    for record in Schedule.select():
        if record.day == day and record.isUpperWeek == is_upper_week():
            schedule.append(f'{record.time} - {record.name}')

    await bot.send_message(message.chat.id, sep.join(schedule))
    log.info('Schedule command from {}'.format(message.from_user.username))


@dp.message_handler(commands=['chatids'])
async def chat_ids_command(message: types.Message):
    await bot.send_message(message.chat.id, chat_ids)
    log.info('Chat IDs command from {}'.format(message.from_user.username))


@dp.message_handler(commands=['week'])
async def week_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Верхняя'if is_upper_week() else 'Нижняя')
    log.info('Week command from {}'.format(message.from_user.username))