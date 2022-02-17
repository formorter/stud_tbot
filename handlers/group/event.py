import asyncio
import logging
from datetime import datetime
from aiogram import types
import os
from db import Database
from loader import dp, bot
from anecdot import Anecdot
"""handler напоминания о предстоящих парах"""
database = Database()  # подключение бд

chat_ids = {}
all_lessons = database.all()  # получение всех документов из бд

# print(database.get({"time": "16:00"})['teacher'])

anecdots = Anecdot()


@dp.message_handler()
async def echo(message: types.Message):
    """Бездарный лог"""
    chat_ids[message.chat.id] = message.from_user
    logging.info(f'Пользователь [{message.chat.username}id={message.chat.id}] подключился')
    # text = f'{message.message_id} {message.from_user} {message.text}'
    # msg = await message.reply('Прив')


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await bot.delete_message(chat_id=os.getenv('GROUP_ID'), message_id=message.message_id)
    logging.info('Сообщение удалено')


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
        logging.info(f'Connected users: {chat_ids}')
        if day_of_week in database.all('day'):
            for lessons in all_lessons:
                if upperWeek is lessons['isUpperWeek']:
                    if day_of_week == lessons['day']:
                        if f"{now}"[11:16] == lessons['time']:
                            print(f'[{now}]'[11:16], f'{lessons["name"]} - ВЫВЕДЕН')
                            msg = await bot.send_message(os.getenv('GROUP_ID'), f"😈 {anecdots.get_random()} 😈\n"
                                                               f"\n Пара {lessons['name']} у {lessons['teacher']} "
                                                               f"\n ссылка на мероприятие: {lessons['links']}",
                                                   disable_notification=True)
                            asyncio.create_task(delete_message(msg, 600))
            else:
                logging.info('Проверка пройдена')
