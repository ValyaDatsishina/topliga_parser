from datetime import date, datetime
import pandas as pd
import openpyxl as xl

from dotenv import main
import os

main.load_dotenv()


def calculate_age(list_of_born):
    today = date.today()
    export_data = []
    for a in list_of_born:
        born = datetime.strptime(a, "%d.%m.%Y").date()
        a = int((today - born).days // 365.2524)
        export_data.append(a)

    return export_data


def data_to_excel(data, parameter_duplicates: str):
    parser_data = os.getenv('PATH_PARSER_DATA')
    if parameter_duplicates == 'all_dataframe':
        data.to_excel(parser_data, index=False)
    elif parameter_duplicates == 'drop_duplicates':
        data = data.drop_duplicates(subset=['Фамилия', 'Имя', 'Электронная почта'])
        data.to_excel(parser_data, index=False)

    print('Данные в таблице')


def filter_age(data, parameter_duplicates: str, ages: list = None):
    list_of_born = data['Дата рождения'].tolist()
    age = []
    age = calculate_age(list_of_born)
    data.insert(loc=6, column='Возраст', value=age)
    pd.set_option('display.max_columns', None)
    # print(data)
    # print(type(age[0]))
    if len(ages) == 1:
        # result_data = data[data['Возраст'].str.contains(f'{age[0]}')]
        result_data = data.loc[data['Возраст'] == int(ages[0])]
        data_to_excel(data=result_data, parameter_duplicates=parameter_duplicates)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    elif len(ages) == 0:
        result_data = data
        data_to_excel(data=result_data, parameter_duplicates=parameter_duplicates)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)

    elif len(ages) == 2:
        if int(ages[0]) < int(ages[1]):
            data = data.loc[data['Возраст'] >= int(ages[0])]
            result_data = data.loc[data['Возраст'] <= int(ages[1])]
            data_to_excel(data=result_data, parameter_duplicates=parameter_duplicates)
        elif int(ages[0]) > int(ages[1]):
            data = data.loc[data['Возраст'] <= int(ages[0])]
            result_data = data.loc[data['Возраст'] >= int(ages[1])]
            data_to_excel(data=result_data, parameter_duplicates=parameter_duplicates)
        elif int(ages[0]) == int(ages[1]):
            result_data = data.loc[data['Возраст'] == int(ages[0])]
            data_to_excel(data=result_data, parameter_duplicates=parameter_duplicates)
    else:
        print('Введите только 2 числа, когда пришете возрат. Дальнейший список будет без фильтра по возрасту')
        result_data = data
        data_to_excel(data=result_data, parameter_duplicates=parameter_duplicates)


def filter_cities(data, parameter_duplicates: str, cities: list = None, ages: list = None):
    if len(cities) == 1:
        result_data = data[data['Город'].str.contains(f'{cities[0]}', case=False)]
        filter_age(data=result_data, ages=ages, parameter_duplicates=parameter_duplicates)
        # age_str = ages[0]
        # print(age_str)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    elif len(cities) == 0:
        result_data = data
        filter_age(data=result_data, ages=ages, parameter_duplicates=parameter_duplicates)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    else:
        list_of_df = []
        for i in cities:
            df = data[data['Город'].str.contains(f'{i}', case=False)]
            list_of_df.append(df)
        result_data = pd.concat(list_of_df)
        filter_age(data=result_data, ages=ages, parameter_duplicates=parameter_duplicates)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)


def filter_gender(data, parameter_duplicates: str, gender: list = None, cities: list = None, ages: list = None):
    if len(gender) == 1:
        result_data = data[data['Пол'].str.contains(f'{gender[0]}', case=False)]
        filter_cities(data=result_data, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    else:
        result_data = data
        filter_cities(data=result_data, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)


def filter_distances(data, parameter_duplicates: str, distances: list = None, gender: list = None, cities: list = None,
                     ages: list = None):
    if len(distances) == 1:
        result_data = data[data['Дистанция'].str.contains(f'{distances[0]}', case=False)]
        filter_gender(data=result_data, gender=gender, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)
        # pd.set_option('display.max_columns', None)  # ввывод всех столбцов df
        # print(result_data)
    elif len(distances) == 0:
        result_data = data
        filter_gender(data=result_data, gender=gender, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)
    else:
        list_of_df = []
        for i in distances:
            df = data[data['Дистанция'].str.contains(f'{i}', case=False)]
            list_of_df.append(df)
        result_data = pd.concat(list_of_df)
        filter_gender(data=result_data, gender=gender, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)


def parsing_events(data, parameter_duplicates: str, events: list = None, distances: list = None, gender: list = None,
                   cities: list = None, ages: list = None):
    if len(events) == 1:
        result_data = data[data['Мероприятие'].str.contains(f'{events[0]}', case=False)]
        filter_distances(data=result_data, distances=distances, gender=gender, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)

    elif len(events) == 0:
        result_data = data
        filter_distances(data=result_data, distances=distances, gender=gender, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)
    else:
        list_of_df = []
        for i in distances:
            df = data[data['Мероприятие'].str.contains(f'{events[i]}', case=False)]
            list_of_df.append(df)
        result_data = pd.concat(list_of_df)
        filter_distances(data=result_data, distances=distances, gender=gender, cities=cities, ages=ages, parameter_duplicates=parameter_duplicates)


def  parsing_date(parameter_duplicates: str, years: list = None, events: list = None, distances: list = None,
                 gender: list = None, cities: list = None, ages: list = None):
    path2 = os.getenv('PATH_FULL_DATA')
    dataFULL = pd.read_excel(path2, sheet_name='Sheet1')
    dataFULL[['Город']] = dataFULL[['Город']].fillna('нет данных')
    # dataFULL = dataFULL.fillna(0)
    # print(dataFULL)

    if len(years) == 1:
        result_data = dataFULL.dropna()[dataFULL.dropna()['Год события'] == int(years[0])]
        parsing_events(data=result_data, events=events, distances=distances, gender=gender, cities=cities, ages=ages,
                       parameter_duplicates=parameter_duplicates)

    elif len(years) == 0:
        result_data = dataFULL
        parsing_events(data=result_data, events=events, distances=distances, gender=gender, cities=cities, ages=ages,
                       parameter_duplicates=parameter_duplicates)
    else:
        list_of_df = []
        for i in years:
            df = dataFULL.dropna()[dataFULL.dropna()['Год события'] == int(i)]
            # df = dataFULL[dataFULL['Год события'].str.contains(f'{years[i]}')]
            list_of_df.append(df)
        result_data = pd.concat(list_of_df)
        parsing_events(data=result_data, events=events, distances=distances, gender=gender, cities=cities, ages=ages,
                       parameter_duplicates=parameter_duplicates)


# Вывод список мероприятий в ТГ
def list_of_events(year):
    path2 = os.getenv('PATH_FULL_DATA')
    dataFULL = pd.read_excel(path2)
    if isinstance(year, list):
        years = []
        for i in year:
            years.append(int(i))

        df = dataFULL[dataFULL['Год события'].isin(years)]
        events = df.Мероприятие.unique().tolist()

        return events

    elif year == 'all':
        events = dataFULL.Мероприятие.unique().tolist()
        return events


def start_filter_telegram(parameter_duplicates, year, event, distance, gender, city, age):
    # path2 = '/Users/valentinabelezak/Downloads/topliga_parser/data/DataFULL.xlsx'
    # dataFULL = pd.read_excel(path2, None)
    # event = input(f'Введите мероприятия из списка через запятую {list(dataFULL.keys())}: ')
    if year == 'all':
        list_of_years = []
    else:
        list_of_years = list(year.split(", "))

    if isinstance(event, list):
        list_of_events = event
    else:
        list_of_events = list(event.split(", "))

    if isinstance(distance, list):
        list_of_distances = distance
    else:
        list_of_distances = list(distance.split(", "))

    # gender = input(f'Введите пол участников: ')
    if gender == []:
        list_of_gender = []
    else:
        list_of_gender = list(gender.split(", "))

    # city = input(f'Введите города: ')
    if isinstance(city, list):
        list_of_cities = city
    else:
        list_of_cities = list(city.split(", "))

    # age = input(f'Введите начальный и финальный возраст через запятую: ')
    if isinstance(age, list):
        list_of_age = age
    else:
        list_of_age = list(age.split("-"))

    return parsing_date(parameter_duplicates, years=list_of_years, events=list_of_events, distances=list_of_distances, gender=list_of_gender,
                        cities=list_of_cities, ages=list_of_age )
# start_filter_telegram('2023', 'Новогодний', '', '', '', '0-14')
