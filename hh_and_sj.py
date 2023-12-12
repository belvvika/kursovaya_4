from vacancy import Vacancy
import requests
from datetime import datetime
class HH(Vacancy):

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





class SJ(Vacancy):

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