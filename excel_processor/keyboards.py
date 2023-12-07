from telebot import types

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

def gender_keyboard():
    gender_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('М')
    item2 = types.KeyboardButton('Ж')
    item3 = types.KeyboardButton('Любой')

    gender_markup.add(item1, item2, item3)

    return gender_markup

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

def age_keyboard():
    age_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Дети')
    item2 = types.KeyboardButton('30-40')
    item3 = types.KeyboardButton('60+')
    item4 = types.KeyboardButton('Любой')

    age_markup.add(item1, item2, item3, item4)

    return age_markup

def parameter_keyboard():
    parameter_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Пропустить')
    item2 = types.KeyboardButton('Удалить дубли')

    parameter_markup.add(item1, item2)

    return parameter_markup
