import json
import os
class Connector:
    """
    Класс коннектор к файлу
    """

    def __init__(self, file_path):
        self.__data_file = file_path
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        """
        if not os.path.exists(self.__data_file):
            with open(self.__data_file, 'w') as file:
                file.write(json.dumps([]))

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, 'r') as file:
            file_data = json.load(file)
        file_data.append(data)
        with open(self.__data_file, 'w') as file:
            json.dump(file_data, file)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        """
        with open(self.__data_file, 'r') as file:
            file_data = json.load(file)

        if not query:
            return file_data

        result = []
        for entry in file_data:
            if all(entry.get(key) == value for key, value in query.items()):
                result.append(entry)
        return result

    def delete(self, query):
        """
        Удаление записей из файла
        """
        if not query:
            return
        with open(self.__data_file, 'r') as file:
            file_data = json.load(file)
        result = []
        for entry in file_data:
            if not all(entry.get(key) == value for key, value in query.items()):
                result.append(entry)
        with open(self.__data_file, 'w') as file:
            json.dump(result, file)
