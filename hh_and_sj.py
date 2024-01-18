from vacancy import Vacancy
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv('.env')
import os

class HH:

    def get_vacancy_hh(self, name):
        list_hh = requests.get(f'{os.getenv("api_hh")}/vacancies',params={'text': name}).json()
        return list_hh

    def vacancies_hh(self, name):
        """Проходим циклом по словарю берем из словаря только нужные нам данные и записываем их в переменную """
        data = self.get_vacancy_hh(name)
        vacancies_hh = []
        for vacancy in data.get('items', []):
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_info = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'salary_from': vacancy['salary']['from'],
                'salary_to': vacancy['salary']['to'],
                'responsibility': vacancy['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            vac = Vacancy(vacancy_info['name'], vacancy_info['responsibility'], vacancy_info['salary_from'])
            # vacancy_data = vac.to_json()

            vacancies_hh.append(vac)

        return vacancies_hh



class SJ:
    def get_vacancy_sj(self, name, title, salary):
        api_key_js = os.getenv('api_sj')
        headers = {
            "X-Api-App-Id": api_key_js,
        }

        list_sj = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params={'name': name, 'title':title, 'salary':salary}).json()
        return list_sj

    def vacancies_sj(self, name, title, salary):
        """Проходим циклом по словарю берем из словаря только нужные нам данные и записываем их в переменную"""
        data = self.get_vacancy_sj(name, title, salary)
        vacancies_sj = []
        for i in data.get('items', []):
            published_at = datetime.strptime(i['date_published'], "%Y-%m-%dT%H:%M:%S%z")
            super_job = {
                'id': i['id_vacancy'],
                'name': i['profession'],
                'salary_from': i['payment_from'],
                'salary_to': i['payment_to'],
                'responsibility': i['candidat'],
                'data': published_at.strftime("%d.%m.%Y"),

            }
            vac = Vacancy(super_job['name'], super_job['responsibility'], super_job['salary_from'])
            vacancy_data = vac.to_json()

            vacancies_sj.append(vac)
        return vacancies_sj

# def to_json(name):
#     data = sj.get_vacancy_sj(name)
#     for i in data:
#         return i['name'], i['responsibility'], i['salary_from']

if __name__ == '__main__':
    # hh = HH()
    # print(hh.get_vacancy_hh('Python'))
    sj = SJ()
    print(sj.get_vacancy_sj('Старший специалист по тестированию', None, 200000))