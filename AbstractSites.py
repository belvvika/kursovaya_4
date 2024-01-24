from abc import ABC, abstractmethod

class ApiSites(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    def load_vacancies(self):
        pass
