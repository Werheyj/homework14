from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button1)
kb.add(button2)
kb.add(button3)

kbI = InlineKeyboardMarkup()
buttonInline1 = InlineKeyboardButton(text='Product1',
                                     callback_data='product_buying')
buttonInline2 = InlineKeyboardButton(text='Product2',
                                     callback_data='product_buying')
buttonInline3 = InlineKeyboardButton(text='Product3',
                                     callback_data='product_buying')
buttonInline4 = InlineKeyboardButton(text='Product4',
                                     callback_data='product_buying')
kbI.add(buttonInline1)
kbI.add(buttonInline2)
kbI.add(buttonInline3)
kbI.add(buttonInline4)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.',
                         reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:',
                         reply_markup=kbI)


products = get_all_products()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    images = ['files/1.jpg', 'files/2.png', 'files/3.jpg', 'files/4.jpg']
    for product in products:
        title, description, price = product
        product_message = f'Название: Product{title} | Описание: описание {description} | Цена: {price}'
        for img_path in images:
            with open(img_path, 'rb') as img:
                await message.answer_photo(img, caption=product_message)
    await message.answer('Выберите продукт для покупки:', reply_markup=kbI)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора: '
                            '10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calorie_calc = (10 * float(data['weight']) +
                    6.25 * float(data['growth']) - 5 * float(data['age']) - 161)
    await message.answer(f'Необходимое количество килокалорий в сутки для вас:'
                         f' {calorie_calc}')

    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
