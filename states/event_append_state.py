from aiogram.dispatcher.filters.state import StatesGroup, State


'''здесь заданы состояния для хендлера добавления новых уведомлений
   first_step - состояние начала создания объявления
   set_new_event - состояние записи объявления в бд
'''


class EventAppendState(StatesGroup):
    set_new_event = State()
