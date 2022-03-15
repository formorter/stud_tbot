from aiogram import types
from database import Schedule
from datetime import datetime
from loader import dp, bot
from utils.misc.logger import logger as log
from handlers.group.event import is_upper_week, chat_ids
from re import split

@dp.message_handler(commands=['ping'])
async def ping_command(message: types.Message):
    await bot.send_message(message.chat.id, 'pong!')
    log.info('Pong command from {}'.format(message.from_user.username))


@dp.message_handler(commands=['schedule'])
async def schedule_command(message: types.Message):
    day = datetime.strftime(datetime.now(), '%A')
    week = is_upper_week()
    sep = '\n' + '-' * 20 + '\n'
    schedule = []
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday', 'Saturday']
    weeks = ['Верхняя', 'Нижняя']

    args = message.get_args()
    
    if isinstance(args, str):
        args = args.split()
    if args:
        if len(args) == 2:
            if args[0] in days:
                if args[1] in weeks:
                    day = args[0]   
                    week = True if args[1] == 'Верхняя' else False
                    schedule.append(f'Расписание на {args[0]}. Неделя: {args[1]}')
                else:
                    day = args[0]
                    schedule.append(f'Неверные входные данные! Выведено расписание на {args[0]} текущей недели!')
            else:
                schedule.append('Неверные входные данные! Выведено расписание на сегодня')
        elif args[0] in days:
            day = args[0]
            schedule.append(f'Расписание на {args[0]} текущей недели')

    for record in Schedule.select():
        if record.day == day and record.isUpperWeek == week:
            schedule.append(f'{record.schedule_id}. {record.time} - {record.name}')


    await bot.send_message(message.chat.id, sep.join(schedule))
    log.info('Schedule command from {}'.format(message.from_user.username))


@dp.message_handler(commands=['edit'])
async def edit_command(message: types.Message):
    args = message.get_args()
    if not args:
        await bot.send_message('Требуются аргументы! /edit [id] (<field:value>) ...')
    args = split('\([^)]*\)', args)
    
    


@dp.message_handler(commands=['chatids'])
async def chat_ids_command(message: types.Message):
    await bot.send_message(message.chat.id, chat_ids)
    log.info('Chat IDs command from {}'.format(message.from_user.username))


@dp.message_handler(commands=['week'])
async def week_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Верхняя'if is_upper_week() else 'Нижняя')
    log.info('Week command from {}'.format(message.from_user.username))