import os
import asyncio
import requests
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


def is_upper_week() -> bool:
    r = requests.request(method='GET', url='http://studydep.miigaik.ru/')
    if r.ok:
        week = r.text.split('неделя:')[1].split()[0]
        if week == "Нижняя":
            log.info(f'Checked site. Is upper returned: {False}')
            return False
        elif week == "Верхняя":
            log.info(f'Checked site. Is upper returned: {True}')
            return True
        else:
            raise Exception('Parse error!')


@dp.message_handler(CommandStart())
async def echo(message: types.Message):
    """Бездарный лог"""
    # print('message handler') # debug
    # log.info(f'Новое сообщение {message.chat.id}, {message.from_user}, {chat_ids}') # debug
    if chat_ids.get(message.chat.id, None):
        chat_ids[message.chat.id] = chat_ids[message.chat.id].append(message.from_user)
    else:
        chat_ids[message.chat.id] = [message.from_user]
        log.info(f'Пользователь [{message.from_user.username}, id={message.chat.id}] подключился')
        log.info(f'Connected users: {chat_ids}')
    # text = f'{message.message_id} {message.from_user} {message.text}'
    # msg = await message.reply('Прив')


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await bot.delete_message(chat_id=os.getenv('GROUP_ID'), message_id=message.message_id)
    log.info('Сообщение {} успешно удалено'.format(message.message_id))


async def periodic(sleep_for):  # основной метод для обработки данных из бд
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.strftime(datetime.now(), "%H:%M")
        day_of_week = datetime.strftime(datetime.now(), "%A")
        _is_upper_week = is_upper_week()
        for lesson in Schedule.select():
            if lesson.time == now and lesson.day == day_of_week and lesson.isUpperWeek == _is_upper_week:
                for chat_id in chat_ids:
                    msg = await bot.send_message(chat_id, f"😈 {anecdots.get_random()} 😈\n"
                                                        f"\n Пара {lesson.name} у {lesson.teacher} "
                                                        f"\n ссылка на мероприятие: {lesson.link}",
                                                        disable_notification=True)
                    log.info(f'{lesson.name}-{now} - ВЫВЕДЕН')
                    asyncio.create_task(delete_message(msg, 600))
        log.info(f'Проверка пройдена. (now:{day_of_week},{now}, upperWeek:{_is_upper_week},\nchats:{chat_ids})')
