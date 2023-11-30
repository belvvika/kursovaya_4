import requests
from datetime import datetime
import json
import os
from abc import ABC, abstractmethod

class ApiSites(ABC):
    @abstractmethod
    def get_api(self):
        pass

class Vacancy:
    def __init__(self, name, description, salary):
        self.name = name
        self.description = description
        self.salary = salary


class Platforms(ApiSites, Vacancy):
    def __init__(self, name, description, salary):
        super().__init__(name, description, salary)

        self.url_hh = 'https://api.hh.ru'
        self.url_sj = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancy_hh(self):
        list_hh = requests.get(f'{self.url_hh}/vacancies',params={'text': self.name, 'description': self.description, 'salary': self.salary}).json()
        return list_hh

    def get_vacancy_sj(self):
        list_sj = requests.get(f'{self.url_sj}/vacancies',params={'text': self.name, 'description': self.description, 'salary': self.salary}).json()
        return list_sj

    def vacancies_hh(self):
        """Проходим циклом по словарю берем из словаря только нужные нам данные и записываем их в переменную """
        data = self.get_vacancy_hh()
        vacancies_hh = []
        for vacancy in data.get('items', []):
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_info = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'solary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'solary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            vacancies_hh.append(vacancy_info)

        return vacancies_hh

    def vacancies_sj(self):
        """Проходим циклом по словарю берем из словаря только нужные нам данные и записываем их в переменную 'vacancy_list_SJ' """
        data = self.get_vacancy_sj()
        vacancy_SJ = []
        for i in data:
            published_at = datetime.fromtimestamp(i.get('date_published', ''))
            super_job = {
                'id': i['id'],
                'name': i.get('profession', ''),
                'solary_ot': i.get('payment_from', '') if i.get('payment_from') else None,
                'solary_do': i.get('payment_to') if i.get('payment_to') else None,
                'responsibility': i.get('candidat').replace('\n', '').replace('•', '') if i.get('candidat') else None,
                'data': published_at.strftime("%d.%m.%Y"),

            }
            vacancy_SJ.append(super_job)
        return vacancy_SJ

def user_interaction():
    name = input('Введите вакансию: ')
    salary = input("Введити желаему заработную плату: ")
    description = input()
    platform = Platforms(name, description, salary)
    combined_dict = {'HH': platform.vacancies_hh(), 'SJ': platform.vacancies_sj()}

    with open('Jobs.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)

    platform.description = description
    hh_data = platform.vacancies_hh()
    sj_data = platform.vacancies_sj()

    combined_dict['HH'] = hh_data
    combined_dict['SJ'] = sj_data

    with open('Jobs.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)

    for platform, data in combined_dict.items():
        print(f"\n \033Платформа: {platform}")
        for item in data:
            print(f"id - {item['id']}\nДолжность - {item['name']}\nЗ.п от - {item['solary_ot']}\nЗ.п до - {item['solary_do']}\nОписание - {item['responsibility']}\nДата - {item['data']}\n")

    a = input('перейти на следующую страницу? y/n ')
    if a == 'y':
        description += 1

if __name__ == "__main__":
    user_interaction()



