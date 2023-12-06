from pathlib import Path

import pandas as pd
import telebot
from dotenv import main
import os
from telebot import types

from excel_processor.fillter_DataFull import start_filter_telegram, list_of_events

main.load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_API_TOKEN'))

users_id = []
for i in range(0, 4):
    users_id.append(int(os.getenv(f'USER_ID_{i}')))
print(users_id)

next_list = ['-', 'дальше', 'далее', 'любое', 'любая', 'любой', 'пропустить']

short_list = ['1 км', '1.5км', '2 км', '2.5 км', ' 3 км']
swim_list = ['Плавание', 'SwimRun']
velo_list = ['велогонк', 'Красная поляна', 'Лаура', 'Русские горки', 'Дуатлон']

# База всех городов и населенных пунктов
path = '/Users/valentinabelezak/Downloads/topliga_parser/data/spisok_gorodov_v_rossii-1021j.xlsx'
data_city = pd.read_excel(path, sheet_name='Sheet2')  # Краснодарский край
krd_list = data_city['Название'].tolist()
data_city = pd.read_excel(path, sheet_name='Sheet1')  # ЮФО
sfd_list = krd_list + data_city['Город'].tolist()
data_city = pd.read_excel(path, sheet_name='Sheet3')  # Москва и область
msk_list = ['Москва'] + data_city['Название'].tolist()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.from_user.id, text=f'Привет! Твой id: {message.from_user.id}')


@bot.message_handler(commands=['parser'], content_types=['text'])
@bot.callback_query_handler(func=lambda call: call.data == 'parser')
def get_start(message):
    if message.from_user.id in users_id:
        test = bot.send_message(message.from_user.id, "Введите год старта:", reply_markup=year_keyboard())
        bot.register_next_step_handler(message, bot_message)
    else:
        bot.send_message(message.from_user.id, "Нет доступа")


def year_keyboard():
    year_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('2019')
    item2 = types.KeyboardButton('2020')
    item3 = types.KeyboardButton('2021')
    item4 = types.KeyboardButton('2022')
    item5 = types.KeyboardButton('2023')
    item6 = types.KeyboardButton('Все года')

    year_markup.add(item1, item2, item3, item4, item5, item6)

    return year_markup


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Все года' or message.text.lower() in next_list:
        year = 'all'
        events_of_year = list_of_events(year)
        text = '\n'.join(events_of_year)
        bot.send_message(message.from_user.id, f'Список мероприятий:\n{text}')
        bot.send_message(message.from_user.id, 'Введите мероприятия через запятую:', reply_markup=event_keyboard())
        bot.register_next_step_handler(message, get_event, year, events_of_year)
    elif message.text == '/parser' or message.text.lower() == 'сначала':
        get_start(message)
    else:
        year = message.text
        list_of_years = list(year.split(", "))
        check_year = all(year.isdigit() for year in list_of_years)
        if check_year is True:
            events_of_year = list_of_events(list_of_years)
            text = '\n'.join(events_of_year)
            bot.send_message(message.from_user.id, f'Список мероприятий:\n{text}')
            bot.send_message(message.from_user.id, 'Введите мероприятия через запятую:', reply_markup=event_keyboard())
            bot.register_next_step_handler(message, get_event, year, events_of_year)
        else:
            bot.send_message(message.from_user.id, "Введите год старта:", reply_markup=year_keyboard())
            bot.register_next_step_handler(message, bot_message)


def event_keyboard():
    event_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('СМ')
    item2 = types.KeyboardButton('СА')
    item3 = types.KeyboardButton('SwimRun')
    item4 = types.KeyboardButton('Город')
    item5 = types.KeyboardButton('Морская Миля')
    item6 = types.KeyboardButton('Ночной')
    item7 = types.KeyboardButton('Beauty run')
    item8 = types.KeyboardButton('ТРИ ГОРЫ')
    item9 = types.KeyboardButton('Любое')

    event_markup.add(item1, item2, item3)
    event_markup.add(item4, item5, item6)
    event_markup.add(item7, item8, item9)

    return event_markup


def get_event(message, year, events_of_year):
    if message.text.lower() in next_list:
        event = []
        bot.send_message(message.from_user.id, 'Введите дистанции: ', reply_markup=dist_keyboard())
        bot.register_next_step_handler(message, get_distance, year, event)
    elif message.text == '/parser' or message.text.lower() == 'сначала':
        get_start(message)
    else:
        list_of_events = list(message.text.split(", "))

        for event in list_of_events:
            check_event = any(event in f for f in events_of_year)
            if check_event is True:
                bot.send_message(message.from_user.id, 'Введите дистанции: ', reply_markup=dist_keyboard())
                bot.register_next_step_handler(message, get_distance, year, list_of_events)
            else:
                print(event)
                print(events_of_year[-1])
                text = '\n'.join(events_of_year)
                events_of_year = events_of_year
                year = year
                text1 = f'Мероприятие введено не верно, введите заново.\nСписок мероприятий:\n{text}'
                bot.send_message(message.from_user.id, text1, reply_markup=event_keyboard())
                bot.register_next_step_handler(message, get_event, year, events_of_year)


def dist_keyboard():
    dist_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('42.2 км')
    item2 = types.KeyboardButton('21.1 км')
    item3 = types.KeyboardButton('10 км')
    item4 = types.KeyboardButton('5 км')
    item5 = types.KeyboardButton('Детская миля')
    item6 = types.KeyboardButton('Короткие дистанции')
    item7 = types.KeyboardButton('Плавание')
    item8 = types.KeyboardButton('Вело')
    item9 = types.KeyboardButton('SwimRun')
    item10 = types.KeyboardButton('Любая')

    dist_markup.add(item1, item2, item3, item4, item5, item6)
    dist_markup.add(item7, item8, item9)
    dist_markup.add(item10)

    return dist_markup


def get_distance(message, year, event):
    if message.text.lower() in next_list:
        distance = []
    elif message.text == 'Короткие дистанции':
        distance = short_list
    elif message.text == 'Плавание':
        distance = swim_list
    elif message.text == 'Вело':
        distance = velo_list
    elif message.text == '/parser' or message.text.lower() == 'сначала':
        distance = 'сначала'
        # bot.register_next_step_handler(message, get_start)
    else:
        distance = message.text

    if distance == 'сначала':
        get_start(message)
    else:
        bot.send_message(message.from_user.id, 'Введите пол участников: ', reply_markup=gender_keyboard())
        bot.register_next_step_handler(message, get_gender, year, event, distance)


def gender_keyboard():
    gender_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('М')
    item2 = types.KeyboardButton('Ж')
    item3 = types.KeyboardButton('Любой')

    gender_markup.add(item1, item2, item3)

    return gender_markup


def get_gender(message, year, event, distance):
    if message.text.lower() == 'М и Ж' or message.text.lower() in next_list:
        gender = []
    elif message.text == '/parser' or message.text.lower() == 'сначала':
        gender = 'сначала'
    else:
        gender = message.text

    if gender == 'сначала':
        get_start(message)
    else:
        bot.send_message(message.from_user.id, 'Введите города: ', reply_markup=city_keyboard())
        bot.register_next_step_handler(message, get_city, year, event, distance, gender)


def city_keyboard():
    city_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Краснодар')
    item2 = types.KeyboardButton('Сочи')
    item3 = types.KeyboardButton('Геленджик')
    item4 = types.KeyboardButton('Анапа')
    item5 = types.KeyboardButton('Москва и МО')
    item6 = types.KeyboardButton('Ростов')
    item7 = types.KeyboardButton('Краснодарский край')
    item8 = types.KeyboardButton('ЮФО')
    item9 = types.KeyboardButton('Любой')

    city_markup.add(item1, item2, item3, item4, item5, item6)
    city_markup.add(item7, item8, item9)

    return city_markup


def get_city(message, year, event, distance, gender):
    if message.text.lower() in next_list:
        city = []
    elif message.text == 'ЮФО':
        city = sfd_list
    elif message.text == 'Краснодарский край':
        city = krd_list
    elif message.text == 'Москва и МО':
        city = msk_list
    elif message.text == 'Краснодар':
        city = ['Краснодар']
    elif message.text == '/parser' or message.text.lower() == 'сначала':
        city = 'сначала'
    else:
        city = message.text

    if city == 'сначала':
        get_start(message)
    else:
        bot.send_message(message.from_user.id, 'Введите начальный и финальный возраст через - без пробелов:',
                         reply_markup=age_keyboard())
        bot.register_next_step_handler(message, get_age, year, event, distance, gender, city)


def age_keyboard():
    age_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Дети')
    item2 = types.KeyboardButton('30-40')
    item3 = types.KeyboardButton('60+')
    item4 = types.KeyboardButton('Любой')

    age_markup.add(item1, item2, item3, item4)

    return age_markup


def get_age(message, year, event, distance, gender, city):
    if message.text.lower() in next_list:
        age = []
    elif message.text == 'Дети':
        age = [0, 14]
    elif message.text == '30-40':
        age = [30, 40]
    elif message.text == '60+':
        age = [60, 200]
    elif message.text == '/parser' or message.text.lower() == 'сначала':
        age = 'сначала'
    else:
        age = message.text
        list_of_ages = list(age.split("-"))
        check_age = all(age.isdigit() for age in list_of_ages)
        if check_age is True:
            age = list_of_ages
        else:
            text = 'Возраст введен не корректно. Введите начальный и финальный возраст через - без пробелов:'
            bot.send_message(message.from_user.id, text, reply_markup=age_keyboard())
            bot.register_next_step_handler(message, get_age, year, event, distance, gender, city)

    if age == 'сначала':
        get_start(message)
    else:
        bot.send_message(message.from_user.id, 'Удалить дубли?',
                         reply_markup=parameter_keyboard())
        bot.register_next_step_handler(message, get_parameter, year, event, distance, gender, city, age)


def parameter_keyboard():
    parameter_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Пропустить')
    item2 = types.KeyboardButton('Удалить дубли')

    parameter_markup.add(item1, item2)

    return parameter_markup


def get_parameter(message, year, event, distance, gender, city, age):
    if message.text.lower() in next_list:
        parameter_dublicate = 'all_dataframe'
    elif message.text == 'Удалить дубли':
        parameter_dublicate = 'drop_duplicates'
    start_filter_telegram(parameter_dublicate, year, event, distance, gender, city, age)
    bot.send_message(message.from_user.id, 'Данные в таблице')
    bot.send_document(message.from_user.id, document=open('Parser_data.xlsx', 'rb'))
    keyboard = telebot.types.InlineKeyboardMarkup()

    button_parser = telebot.types.InlineKeyboardButton(text="Начать сначала",
                                                       callback_data='parser')
    keyboard.add(button_parser)
    bot.send_message(message.from_user.id,
                     'Начнем заново?',
                     reply_markup=keyboard)


bot.infinity_polling(none_stop=True)
