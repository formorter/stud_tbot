import os
import asyncio
import logging
import sys
from database import Schedule
from datetime import datetime
from tabnanny import verbose
from aiogram import types
from loader import dp, bot
from anecdot import Anecdot
"""handler напоминания о предстоящих парах"""

chat_ids = {}
all_lessons = [record.as_dict() for record in Schedule.select()]  # получение всех документов из бд

anecdots = Anecdot()

def log(text: str):
    logging.info(text)
    if '-v' in sys.argv:
        print(text)

@dp.message_handler()
async def echo(message: types.Message):
    """Бездарный лог"""
    chat_ids[message.chat.id] = message.from_user
    log(f'Пользователь [{message.chat.username}id={message.chat.id}] подключился')
    # text = f'{message.message_id} {message.from_user} {message.text}'
    # msg = await message.reply('Прив')


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await bot.delete_message(chat_id=os.getenv('GROUP_ID'), message_id=message.message_id)
    log('Сообщение удалено')


async def periodic(sleep_for):  # основной метод для обработки данных из бд
    with open('data/conf.txt', 'r') as f:
        data = f.readline()
        upperWeek = bool(data.split('=')[1])
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.now()
        day_of_week = now.strftime('%A')
        if day_of_week == 'Monday' and f'{now}'[11:16] == '00:00':
            with open('data/conf.txt', 'w') as f:
                upperWeek = not upperWeek
                data = f'upperWeek={upperWeek}'
                f.write(data)
        log(f'Connected users: {chat_ids}')
        if day_of_week in [record.day for record in Schedule.select()]:
            for lesson in all_lessons:
                if upperWeek is lesson['isUpperWeek']:
                    if day_of_week == lesson['day']:
                        if f"{now}"[11:16] == lesson['time']:
                            print(f'[{now}]'[11:16], f'{lesson["name"]} - ВЫВЕДЕН')
                            msg = await bot.send_message(os.getenv('GROUP_ID'), f"😈 {anecdots.get_random()} 😈\n"
                                                               f"\n Пара {lesson['name']} у {lesson['teacher']} "
                                                               f"\n ссылка на мероприятие: {lesson['links']}",
                                                   disable_notification=True)
                            asyncio.create_task(delete_message(msg, 600))
            else:
                log('Проверка пройдена')
