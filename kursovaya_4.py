import requests
from datetime import datetime
import json
import os
from abc import ABC, abstractmethod

class ApiSites(ABC):
    @abstractmethod
    def __init__(self):
        self.api_hh = 'https://api.hh.ru'
        self.api_sj = 'https://api.superjob.ru/2.0/vacancies/'

class Vacancy:
    def __init__(self, name, title, salary):
        self.name = name
        self.title = title
        self.salary = salary

    def __repr__(self):
        return f"Vacancy(name='{self.name}', title='{self.title}', salary='{self.salary}')"

    def __str__(self):
        return self.title

    def __gt__(self, other):
        return self.salary > other.salary

    def __lt__(self, other):
        if other.salary is None:
            return False
        if self.salary is None:
            return True
        return self.salary < other.salary


# if __name__ == '__main__':
#     v1 = Vacancy('name', 'title', 'salary')
#
#     v2 = Vacancy('name', 'title', 'salary')
#
#     v3 = Vacancy('name', 'title', 'salary')
#
#     vacancies = [v1, v2, v3]
#
#     vv = sorted(vacancies)
#
#     print(vv)

class HH(ApiSites, Vacancy):
    def __init__(self, name, title, salary):
        super().__init__(name, title, salary)

    def get_vacancy_hh(self):
        try:
            list_hh = requests.get(f'{self.api_hh}/vacancies',params={'name': self.name, 'title': self.title, 'salary': self.salary}).json()
            return list_hh
        except requests.exceptions.HTTPError as errh:
            print("Такой страницы не существует.")
            print(errh.args[0])

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

class SJ(ApiSites, Vacancy):
    def __init__(self, name, title, salary):
        super().__init__(name, title, salary)

    def get_vacancy_sj(self):
        try:
            list_sj = requests.get(f'{self.api_sj}/vacancies',params={'name': self.name, 'title': self.title, 'salary': self.salary}).json()
            return list_sj
        except requests.exceptions.HTTPError as errh:
            print("Такой страницы не существует.")
            print(errh.args[0])
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
def json_file():
    with open('Jobs.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)

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

    json_file()

    for platform, data in combined_dict.items():
        print(f"\n \033Платформа: {platform}")
        for item in data:
            print(f"id - {item['id']}\nДолжность - {item['name']}\nЗ.п от - {item['solary_ot']}\nЗ.п до - {item['solary_do']}\nОписание - {item['responsibility']}\nДата - {item['data']}\n")

    a = input('перейти на следующую страницу? y/n ')
    if a == 'y':
        title += 1

if __name__ == "__main__":
    user_interaction()



