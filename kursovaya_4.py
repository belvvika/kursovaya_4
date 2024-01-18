import requests
from datetime import datetime
import json
from AbstractSites import ApiSites
from vacancy import Vacancy
from connect import Connector
from hh_and_sj import HH, SJ

# def json_file():
#     with open('Jobs.json', 'w', encoding='utf-8') as file:
#         json.dump(combined_dict, file, ensure_ascii=False, indent=2)

def user_interaction():
    title = input('Введите вакансию: ')

    filename = input('Путь сохранения файла')

    #получение данных hh, sj
    hh = HH()
    vacancy_hh = hh.vacancies_hh(title)
    # sj = SJ()
    # vacancyss_sj = sj.vacancies_sj(title)
    #валидация  (превратить список словарей в список вакансий)

    connect = Connector(filename)
    connect.insert(vacancy_hh)
    # connect.insert(vacancyss_sj)
    #сохранение вакансий
    #сортировка и поиск

if __name__ == "__main__":
    user_interaction()



