import pandas as pd
import enchant
import openpyxl as xl
import os
from datetime import date, datetime

import xlrd
from translate import Translator

def delete_prefix(list_of_cities: list) -> list:
    prefix_of_cities = ['Город', 'город', 'Г', 'Г.', 'г', 'г.', 'с', 'с.', 'д', 'д.', 'п', 'п.', 'р-н', 'район', 'рп',
                        'рп.', 'пгт.', 'пгт', 'ст-ца', 'х.', 'х', 'тер.', 'нп', 'мкр', 'мкр.', 'обл', 'обл.']
    export_data = []
    for city in list_of_cities:
        if city == 0:
            city = ''

        elif type(city) == str:
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

def clean_distances(list_of_distances: list):
    print(list_of_distances)
    print(len(list_of_distances))
    export_data = []
    for distance in list_of_distances:
        if distance == 0:
            distance = ''
        elif 'Детский' in distance or 'детский' in distance:
            distance = 'Детская миля'
        elif 'Детская миля' in distance:
            distance = 'Детская миля'
        elif '42' in distance:
            distance = '42.2 км'
        elif '21' in distance and 'Эстафета' not in distance:
            distance = '21.1 км'
        elif '10' in distance and 'км' in distance:
            distance = '10 км'
        elif 'Laura' in distance:
            distance = 'Лаура'
        elif 'Online' in distance:
            distance = 'Онлайн'
        elif 'SWIMRUN' in distance and 'Sprint' not in distance:
            distance = 'SwimRun'
        elif 'SWIMRUN' in distance and 'Sprint' in distance:
            distance = 'SwimRun Sprint'
        elif 'эстафета 2*5 км' in distance or 'Эстафета 2х5 км' in distance:
            distance = 'эстафета 2 х 5 км'
        elif distance == '2 км, с футболкой, 12+':
            distance = '2 км'
        else:
            distance = distance


        export_data.append(distance)
    print(export_data)
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


def add_data(path):
    path2 = '/Users/valentinabelezak/Downloads/topliga_parser/data/DataFULL.xlsx'
    data = pd.read_excel(path)
    data[['Дистанция','Фамилия', 'Имя']] = data[['Дистанция','Фамилия', 'Имя']].fillna(0)
    data = data[data.Фамилия != 0]
    dataFULL = pd.read_excel(path2, None)
    columns = ['Дистанция', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Пол', 'Город', 'Мобильный телефон',
               'Электронная почта']
    # print(list(dataFULL.keys()))


    check = check_columns(data, columns)
    if check != True:
        if len(check) == 1:
            print(f'Отсутствует колонка {check[0]}')
        else:
            columns = ', '.join(check)
            print(f'Отсутствуют колонки {columns}')
    else:
        new_data = data[columns]

        list_of_cities = new_data['Город'].tolist()
        cities = []
        cities = delete_prefix(list_of_cities)
        new_data.pop('Город')
        new_data.insert(loc=6, column='Город', value=cities)

        list_of_distances = new_data['Дистанция'].tolist()
        distances = clean_distances(list_of_distances)
        new_data.pop('Дистанция')



        sheet_name = os.path.splitext(os.path.basename(path))[0].split(' ')
        sheet_name.pop(-1)
        evetn = ''
        for i in sheet_name:
            evetn += str(i)
            evetn += ' '
        print(evetn)
        year = os.path.splitext(os.path.basename(path))[0].split(' ')[-1]

        new_data.insert(loc=0, column='Мероприятие', value=evetn)
        new_data.insert(loc=1, column='Год события', value=year)
        new_data.insert(loc=2, column='Дистанция', value=distances)


        new_data = new_data.drop_duplicates(subset=['Мероприятие', 'Дистанция', 'Фамилия', 'Имя', 'Отчество'])

        pd.set_option('display.max_columns', None) #ввывод всех столбцов df
        print(new_data.head(10))
        with pd.ExcelWriter(path2, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
            new_data.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, header=None, index=False)




path1 = '/Users/valentinabelezak/Downloads/topliga_parser/data/Автодром 2023.xlsx'
path2 = '/Users/valentinabelezak/Downloads/topliga_parser/data/DataFULL.xlsx'
path3 = '/Users/valentinabelezak/Downloads/topliga_parser/data/Хард ран 2020.xls'
path_error = '/Users/valentinabelezak/Downloads/topliga_parser/data/Календарь 2023 - рабочий.xlsx'

# add_date('/Users/valentinabelezak/Downloads/topliga_parser/data/Data_2023/СМ 2023.xls')

# list_of_name_events = os.listdir('/Users/valentinabelezak/Downloads/topliga_parser/data/Data_2019/')
add_data(f'/Users/valentinabelezak/Downloads/topliga_parser/data/Data_2023/СА 2023.xls')
# for i in [23]:
#     path = f'/Users/valentinabelezak/Downloads/topliga_parser/data/Data_20{i}/'
#     list_of_name_events = os.listdir(f'/Users/valentinabelezak/Downloads/topliga_parser/data/Data_20{i}/')
#     for j in list_of_name_events:
#
#         if j.split('.')[-1] == 'xls' or j.split('.') == 'xlsx':
#             add_data(f'{path}{j}')

# print(os.listdir('/Users/valentinabelezak/Downloads/topliga_parser/data/Data_2021/'))