import os
import asyncio
from utils.misc.logger import logger as log
from database import Schedule
from datetime import datetime
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from anecdot import Anecdot
"""handler напоминания о предстоящих парах"""

chat_ids = {}

anecdots = Anecdot()

@dp.message_handler(CommandStart())
async def echo(message: types.Message):
    """Бездарный лог"""
    # print('message handler') # debug
    # log.info(f'Новое сообщение {message.chat.id}, {message.from_user}, {chat_ids}') # debug
    if chat_ids.get(message.chat.id, None):
        chat_ids[message.chat.id] = chat_ids[message.chat.id].append(message.from_user)
    else:
        chat_ids[message.chat.id] = [message.from_user]
        log.info(f'Пользователь [{message.chat.username}, id={message.chat.id}] подключился')
        log.info(f'Connected users: {chat_ids}')
    # text = f'{message.message_id} {message.from_user} {message.text}'
    # msg = await message.reply('Прив')


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await bot.delete_message(chat_id=os.getenv('GROUP_ID'), message_id=message.message_id)
    log.info('Сообщение {} успешно удалено'.format(message.message_id))


async def periodic(sleep_for):  # основной метод для обработки данных из бд
    with open('data/conf.txt', 'r') as f:
        data = f.readline()
        upperWeek = bool(data.split('=')[1])
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.now()
        day_of_week = now.strftime('%A')
        if day_of_week == 'Monday' and datetime.strftime(now,"%H:%M") == '00:00':
            with open('data/conf.txt', 'w') as f:
                upperWeek = not upperWeek
                data = f'upperWeek={upperWeek}'
                f.write(data)
        for lesson in Schedule.select():
            if lesson.date == f'{now}, {day_of_week}' and lesson.isUpperWeek == upperWeek:
                msg = await bot.send_message(os.getenv('GROUP_ID'), f"😈 {anecdots.get_random()} 😈\n"
                                                    f"\n Пара {lesson.name} у {lesson.teacher} "
                                                    f"\n ссылка на мероприятие: {lesson.link}",
                                                    disable_notification=True)
                print(datetime.strftime(now, "%H:%M"), f'{lesson.name} - ВЫВЕДЕН')
                asyncio.create_task(delete_message(msg, 600))
        log.info(f'Проверка пройдена')