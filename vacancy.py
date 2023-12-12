from ABC import ApiSites

class Vacancy(ApiSites):
    def __init__(self, name, title, salary):
        self.name = name
        self.title = title
        self.salary = salary
        self.api_hh = 'https://api.hh.ru'
        self.api_sj = 'https://api.superjob.ru/2.0/vacancies/'

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