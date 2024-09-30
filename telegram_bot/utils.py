from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp


API_REGISTER_URL = 'http://127.0.0.1:8000/api/auth/users/'
API_TOKEN_URL = 'http://127.0.0.1:8000/api/auth/jwt/'

USER_ID = 0
ACCESS = {'username': '', 'password': ''}
DATA = {'access': '', 'refresh': ''}


# def generate_calendar(year: int, month: int):
#     keyboard = InlineKeyboardMarkup(row_width=7)
#     days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#     keyboard.add(*[InlineKeyboardButton(day, callback_data='ignore') for day in days_of_week])

#     first_day_of_month = datetime(year, month, 1)
#     next_month = first_day_of_month + timedelta(days=32)
#     last_day_of_month = next_month.replace(day=1) - timedelta(days=1)

#     day = first_day_of_month
#     while day.weekday() != 0:
#         day -= timedelta(days=1)

#     while day <= last_day_of_month:
#         row = []
#         for _ in range(7):
#             if day.month == month:
#                 row.append(InlineKeyboardButton(str(day.day), callback_data=f"day_{day.day}"))
#             else:
#                 row.append(InlineKeyboardButton(" ", callback_data="ignore"))
#             day += timedelta(days=1)
#         keyboard.add(*row)

#     prev_month = first_day_of_month - timedelta(days=1)
#     next_month = last_day_of_month + timedelta(days=1)
#     keyboard.add(
#         InlineKeyboardButton("<<", callback_data=f"change_month_{prev_month.year}_{prev_month.month}"),
#         InlineKeyboardButton(">>", callback_data=f"change_month_{next_month.year}_{next_month.month}")
#     )

#     return keyboard


def generate_tags(tags_data):
    keyboard = InlineKeyboardMarkup(row_width=5)
    callback_data_list = [{
        'id': tag.id,
        'name': tag.name,
        'slug': tag.slug
    } for tag in tags_data]
    keyboard.add(*[InlineKeyboardButton(
        callback_data['name'], callback_data=callback_data
    ) for callback_data in callback_data_list])

    return keyboard


async def register_user():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            API_REGISTER_URL,
            json={'username': ACCESS['username'],
                  'password': ACCESS['password']}
        ) as response:
            if response.status == 201:
                data = await response.json()
                USER_ID = data['id']
                return
            else:
                async with session.post(
                    f'{API_TOKEN_URL}refresh/',
                    json={'refresh': DATA['refresh']}
                ) as response:
                     data = await response.json()
                     DATA['access'] = data['access']
                     return
            

async def get_jwt_token():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{API_TOKEN_URL}create/',
            json={'username': ACCESS['username'],
                  'password': ACCESS['password']}
        ) as response:
            if response.status == 200:
                data = await response.json()
                DATA['access'] = data['access']
                DATA['refresh'] = data['refresh']
                return
            else:
                return