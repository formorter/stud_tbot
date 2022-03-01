from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types
from states import EventAppendState


@dp.message_handler(commands=['event_add'])
async def first_step(message: types.Message):
    await EventAppendState.set_new_event.set()
    await message.answer(text='🌈🌈🌈 СОЗДАНИЕ СОБЫТИЯ 🌈🌈🌈'
                              'Привет, ты хочешь создать уведомление? Шикарно, заполни форму:'
                              '\n1.Название пары:'
                              '\n1.Имя преподавателя:'
                              '\n2.День недели:'
                              '\n3.Верхняя или нижняя неделя:'
                              '\n4.Ссылка на мероприятие:'
                              '\n5.В какое время отправить уведомление:')


@dp.message_handler(state=EventAppendState.set_new_event)
async def set_event(message: types.Message, state: FSMContext):
    msg = message.text
    splited_message = (msg.split('\n'))
    print(splited_message)
    for args in splited_message:
        print(args.split(':'))
    await message.answer(text='😎Твоё событие создано, жесть ты крут😎')
    await state.finish()



