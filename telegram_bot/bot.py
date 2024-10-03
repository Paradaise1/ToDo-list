import logging
import aiohttp
import requests

from datetime import datetime
from pytz import timezone

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from .utils import (
    generate_tags,
    register_user,
    get_jwt_token,
    ACCESS,
    DATA,
)

API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
AMERICA = timezone('America/Adak')
API_URL = 'http://127.0.0.1:8000/api'

USER_ID = 0
TAG_LIST = []
HEADERS = dict()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# @dp.message_handler(commands='start')
# async def start(message: types.Message):
#     now = datetime.now(AMERICA)
#     keyboard = generate_calendar(now.year, now.month)
#     await message.answer("Please select a date:", reply_markup=keyboard)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('''Привет! Я ваш помощник по управлению задачами. 
                        Введите имя пользователя и пароль:''')
    
    @dp.message_handler(commands=['addtask'])
    async def get_access(msg: types.Message):
        global USER_ID, HEADERS
        username, password = msg.text.split()
        username.strip(',')
        password.strip()
        ACCESS['username'] = username
        ACCESS['password'] = password
        idd = register_user()
        if idd.isinstance(int):
            USER_ID = idd
        get_jwt_token()
        headers = {'Authorization': f'Bearer {DATA["access"]}'}
        HEADERS = {k:v for k, v in headers.items()}
        await msg.reply('Используйте команды /tasks для просмотра задач '
                        'и /addtask для добавления новой задачи.')


@dp.message_handler(commands=['tasks'])
async def list_tasks(message: types.Message):
    response = requests.get(f'{API_URL}/tasks/', headers=HEADERS)
    tasks = response.json()
    if tasks:
        tasks_list = []
        for task in task:
            completed = 'Да!' if task.completed else 'Нет.'
            tag_list = [tag for tag in task['tags']]
            msg_task = (f'{task["id"]}: {task["title"]}\n'
                        f'Тэги: {tag_list}\n'
                        f'Завершена: {completed}\n'
                        f'Дата завершения: {task.completion_date}\n'
                        f'Задача: {task.description}')
            tasks_list.append(msg_task)
        await message.reply(f'Ваши задачи:\n{tasks_list}')
    else:
        await message.reply('У вас нет задач.')


@dp.message_handler(commands=['addtask'])
async def add_task(msg: types.Message):
    await msg.reply('Введите название задачи:')

    @dp.message_handler()
    async def get_completion_date(msg: types.Message):
        title = msg.text
        await msg.reply('Введите дату завершения задачи в формате '
                        'DD:MM:YY (часовой пояс GMT -9:00) :')

        @dp.message_handler()
        async def get_task_title(msg: types.Message):
            completion_date = msg.text
            if datetime.strptime(
                completion_date, '%d-%b-%Y'
            ).date() < datetime.now(AMERICA):
                completed = True
            else:
                completed = False

            response = requests.get(f'{API_URL}/tags/', headers=HEADERS)
            tags = response.json()
            keyboard = generate_tags(tags)
            await msg.answer(
                'Выберите тэги для задачи:', reply_markup=keyboard
            )

            @dp.callback_query_handler(lambda call: True)
            async def gat_tag_list(call: types.CallbackQuery):
                TAG_LIST.append(call.data)

            @dp.message_handler()
            async def get_task_tags(msg: types.Message):
                json_data = {
                    'title': title,
                    'author': USER_ID,
                    'completion_date': completion_date,
                    'completed': completed,
                    'tags': TAG_LIST
                }
                response = requests.post(
                    f'{API_URL}/tasks/', headers=HEADERS, json=json_data
                )
                if response.status_code == 201:
                    await msg.reply('Задача успешно добавлена!')
                else:
                    await msg.reply('Произошла ошибка при добавлении задачи.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
