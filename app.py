import asyncio
import handlers
from aiogram import executor
from loader import dp

from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(handlers.group.event.periodic(60))
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
