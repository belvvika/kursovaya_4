from abc import ABC, abstractmethod
import json
import time
import requests
import os
class ApiSites(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    def load_vacancies(self):
        pass
