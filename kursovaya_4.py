
from connect import Connector
from hh_and_sj import HH, SJ


def user_interaction():
    title = input('Введите вакансию: ')

    filename = input('Путь сохранения файла: ')

    #получение данных hh, sj
    hh = HH()
    vacancy_hh = hh.vacancies_hh(title)
    sj = SJ()
    vacancyss_sj = sj.vacancies_sj(title)
    #валидация  (превратить список словарей в список вакансий)

    connect = Connector(filename)
    connect.insert(vacancy_hh)
    connect.insert(vacancyss_sj)
    #сохранение вакансий
    #сортировка и поиск

if __name__ == "__main__":
    user_interaction()



