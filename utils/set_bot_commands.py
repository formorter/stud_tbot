from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("event_add", "Добавить уведомление"),
            types.BotCommand("week", "Отобразить тип недели"),
            types.BotCommand("ping", "pong!"),
            types.BotCommand("schedule", "Вывести расписание на сегодняшний день"),
            types.BotCommand("chatids", "Выводит список Chat IDs"),
        ]
    )
