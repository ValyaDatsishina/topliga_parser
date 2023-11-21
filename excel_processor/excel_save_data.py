# import openpyxl as xl
# import os
# path1 = '/Users/valentinabelezak/Downloads/topliga_parser/data/liga.xlsx'
# path2 = '/Users/valentinabelezak/Downloads/topliga_parser/excel_processor/DataFULL.xlsx'
#
#
# # wb1 = xl.load_workbook(filename=path1)
# # ws1 = wb1.worksheets[0]
#
# wb2 = xl.load_workbook(filename=path2)
# ws2 = wb2.create_sheet(path1)
# # ws2 = wb2.create_sheet(os.path.basename(path1))
# ws2.appand('Дистанция','Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Пол', 'Город', 'Мобильный телефон', 'Электронная почта')
#
# # for row in ws2:
# #     for cell in row:
# #         ws1[cell.coordinate].value = cell.value
#
# wb2.save(path2)

import pandas as pd
import enchant
import openpyxl as xl
import os
from datetime import date, datetime

import xlrd
from translate import Translator


def delete_prefix(list_of_cities: list) -> list:
    prefix_of_cities = ['г', 'г.', 'с', 'с.', 'д', 'д.', 'п', 'п.', 'рп', 'рп.', 'пгт.', 'пгт', 'ст-ца']
    export_data = []
    for city in list_of_cities:

        if type(city) == str:
            trans = enchant.Dict("en_US")
            if trans.check(city):
                translator = Translator(from_lang="English", to_lang="Russian")
                city = translator.translate(city)

            new_str = city.split()

            if len(new_str) == 2:
                if new_str[0] in prefix_of_cities:
                    city = new_str[1:][0]
                if new_str[-1] in prefix_of_cities:
                    city = new_str[:-1][0]

            if len(new_str) > 2:
                if new_str[0] in prefix_of_cities:
                    city = ' '.join(new_str[1:])
                if new_str[-1] in prefix_of_cities:
                    city = ' '.join(new_str[:-1])
        else:
            city = ''

        export_data.append(city)

    # print(export_data)
    return export_data

def check_columns(data, columns: list):
    n = 0
    list_of_not_column = []
    for column in columns:
        if column in data.columns.tolist():
            n += 1
        else:
            list_of_not_column.append(column)
    if len(columns) == n:
        return True
    else:
        return list_of_not_column


def add_date(path):
    path2 = '/Users/valentinabelezak/Downloads/topliga_parser/data/DataFULL.xlsx'
    data = pd.read_excel(path)
    data = data.fillna(method='ffill', axis=0)
    dataFULL = pd.read_excel(path2, None)
    columns = ['Дистанция', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Пол', 'Город', 'Мобильный телефон',
               'Электронная почта']
    print(list(dataFULL.keys()))


    check = check_columns(data, columns)
    if check != True:
        if len(check) == 1:
            print(f'Отсутствует колонка {check[0]}')
        else:
            columns = ', '.join(check)
            print(f'Отсутствуют колонки {columns}')
    elif os.path.splitext(os.path.basename(path))[0] in list(dataFULL.keys()):
        print(f'Таблица {os.path.splitext(os.path.basename(path))[0]} уже загружена. Переименуйте файл или загрузите новый')
    else:
        new_data = data[columns]

        list_of_cities = new_data['Город'].tolist()
        cities = []
        cities = delete_prefix(list_of_cities)
        new_data.pop('Город')
        new_data.insert(loc=6, column='Город', value=cities)

        new_data = new_data.drop_duplicates(subset=['Дистанция', 'Фамилия', 'Имя', 'Отчество'])

        pd.set_option('display.max_columns', None) #ввывод всех столбцов df
        print(new_data.head(10))
        with pd.ExcelWriter(path2, engine='openpyxl', mode='a') as writer:
            new_data.to_excel(writer, sheet_name=os.path.splitext(os.path.basename(path))[0])




path1 = '/Users/valentinabelezak/Downloads/topliga_parser/data/Автодром 2023.xlsx'
path2 = '/Users/valentinabelezak/Downloads/topliga_parser/data/DataFULL.xlsx'
path3 = '/Users/valentinabelezak/Downloads/topliga_parser/data/Хард ран 2020.xls'
path_error = '/Users/valentinabelezak/Downloads/topliga_parser/data/Календарь 2023 - рабочий.xlsx'

add_date('/Users/valentinabelezak/Downloads/topliga_parser/Data_2023/Сочи Марафон 2023.xls')
# data = pd.read_excel(path2)
# data = data.fillna(method='ffill', axis=0)
# data=data.drop_duplicates(subset=['Дистанция', 'Фамилия', 'Имя', 'Отчество'])
# pd.set_option('display.max_columns', None)
# print(data.head(10))

# print(list_of_cities[-1])
