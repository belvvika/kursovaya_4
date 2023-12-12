import requests
from datetime import datetime
import json

from vacancy import Vacancy
from connect import Connector
from hh_and_sj import HH,SJ

# def json_file():
#     with open('Jobs.json', 'w', encoding='utf-8') as file:
#         json.dump(combined_dict, file, ensure_ascii=False, indent=2)

def user_interaction():
    name = input('Введите вакансию: ')
    salary = input("Введити желаему заработную плату: ")
    title = input()
    hh = HH(name, title, salary)
    sj = SJ(name, title, salary)
    combined_dict = {'HH': hh.vacancies_hh(), 'SJ': sj.vacancies_sj()}
    hh_data = hh.vacancies_hh()
    sj_data = sj.vacancies_sj()
    hh.title = title
    sj.title = title
    combined_dict['HH'] = hh_data
    combined_dict['SJ'] = sj_data

    # json_file()

    with open('Jobs.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)

    for platform, data in combined_dict.items():
        print(f"\n \033Платформа: {platform}")
        for item in data:
            print(f"id - {item['id']}\nДолжность - {item['name']}\nЗ.п от - {item['solary_ot']}\nЗ.п до - {item['solary_do']}\nОписание - {item['responsibility']}\nДата - {item['data']}\n")

    a = input('перейти на следующую страницу? y/n ')
    if a == 'y':
        title += 1

if __name__ == "__main__":
    user_interaction()



