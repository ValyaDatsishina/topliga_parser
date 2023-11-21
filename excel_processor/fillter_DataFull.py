from datetime import date, datetime
import pandas as pd


def calculate_age(list_of_born):
    today = date.today()
    export_data = []
    for a in list_of_born:
        born = datetime.strptime(a, "%d.%m.%Y").date()
        a = int((today - born).days // 365.2524)
        export_data.append(str(a))

    return export_data


def data_to_excel(data):
    parser_data = '/Users/valentinabelezak/Downloads/topliga_parser/data/Parser_data.xlsx'
    data.to_excel(parser_data, index=False)
    print('Данные в таблице')


def filter_age(data, ages: list = None):
    list_of_born = data['Дата рождения'].tolist()
    age = []
    age = calculate_age(list_of_born)
    data.insert(loc=6, column='Возраст', value=age)
    pd.set_option('display.max_columns', None)
    # print(data)
    # print(type(age[0]))
    if len(ages) == 1:
        # result_data = data[data['Возраст'].str.contains(f'{age[0]}')]
        result_data = data.loc[data['Возраст'] > ages[0]]
        data_to_excel(data=result_data)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    elif len(ages) == 0:
        result_data = data
        data_to_excel(data=result_data)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)

    elif len(ages) == 2:
        if ages[0] < ages[1]:
            data = data.loc[data['Возраст'] > ages[0]]
            result_data = data.loc[data['Возраст'] < ages[1]]
            data_to_excel(data=result_data)
        elif ages[0] > ages[1]:
            data = data.loc[data['Возраст'] < ages[0]]
            result_data = data.loc[data['Возраст'] > ages[1]]
            data_to_excel(data=result_data)
    else:
        print('Введите только 2 числа, когда пришете возрат. Фильтрация по возрасту не делается')
        result_data = data
        data_to_excel(data=result_data)


def filter_cities(data, cities: list = None, ages: list = None):
    if len(cities) == 1:
        result_data = data[data['Город'].str.contains(f'{cities[0]}')]
        filter_age(data=result_data, ages=ages)
        age_str = ages[0]
        print(age_str)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    elif len(cities) == 0:
        result_data = data
        filter_age(data=result_data, ages=ages)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    else:
        list_of_df = []
        for i in cities:
            df = data[data['Город'].str.contains(f'{i}')]
            list_of_df.append(df)
        result_data = pd.concat(list_of_df)
        filter_age(data=result_data, ages=ages)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)


def filter_gender(data, gender: list = None, cities: list = None, ages: list = None):
    if len(gender) == 1:
        result_data = data[data['Пол'].str.contains(f'{gender[0]}')]
        filter_cities(data=result_data, cities=cities, ages=ages)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    else:
        result_data = data
        filter_cities(data=result_data, cities=cities, ages=ages)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)


def filter_distances(data, distances: list = None, gender: list = None, cities: list = None, ages: list = None):
    if len(distances) == 1:
        result_data = data[data['Дистанция'].str.contains(f'{distances[0]}')]
        filter_gender(data=result_data, gender=gender, cities=cities, ages=ages)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    elif len(distances) == 0:
        result_data = data
        filter_gender(data=result_data, gender=gender, cities=cities, ages=ages)
    else:
        list_of_df = []
        for i in distances:
            df = data[data['Дистанция'].str.contains(f'{i}')]
            list_of_df.append(df)
        result_data = pd.concat(list_of_df)
        filter_gender(data=result_data, gender=gender, cities=cities, ages=ages)


def parsing_data(events: list = None, distances: list = None, gender: list = None, cities: list = None,
                 ages: list = None):
    path2 = '/Users/valentinabelezak/Downloads/topliga_parser/data/DataFULL.xlsx'
    dataFULL = pd.read_excel(path2, None)

    if len(events) == 1:
        data = pd.read_excel(path2, sheet_name=events[0])
        filter_distances(data=data, distances=distances, gender=gender, cities=cities, ages=ages)

    elif len(events) == 0:
        list_of_df = []
        full_events = list(dataFULL.keys())

        for i in full_events:
            df = pd.read_excel(path2, sheet_name=i)
            list_of_df.append(df)
        data = pd.concat(list_of_df)
        filter_distances(data=data, distances=distances, gender=gender, cities=cities, ages=ages)

    else:
        list_of_df = []
        for i in events:
            df = pd.read_excel(path2, sheet_name=i)
            list_of_df.append(df)
        data = pd.concat(list_of_df)
        filter_distances(data=data, distances=distances, gender=gender, cities=cities, ages=ages)


def start_filter():
    path2 = '/Users/valentinabelezak/Downloads/topliga_parser/data/DataFULL.xlsx'
    dataFULL = pd.read_excel(path2, None)
    event = input(f'Введите мероприятия из списка через запятую {list(dataFULL.keys())}: ')
    if event == '':
        list_of_events = []
    else:
        list_of_events = list(event.split(", "))

    distance = input(f'Введите дистанции: ')
    list_of_distances = list(distance.split(", "))

    gender = input(f'Введите пол участников: ')
    list_of_gender = list(gender.split(", "))

    city = input(f'Введите города: ')
    list_of_cities = list(city.split(", "))

    age = input(f'Введите начальный и финальный возраст через запятую: ')
    list_of_age = list(age.split(", "))

    return parsing_data(events=list_of_events, distances=list_of_distances, gender=list_of_gender,
                        cities=list_of_cities, ages=list_of_age)


start_filter()
