import csv
import os
import re
from abc import ABC, abstractmethod

from utils.class_operations import Vacancy


class Adder(ABC):
    """Абстрактный класс для добавления вакансий в файл в формате csv."""

    @staticmethod
    @abstractmethod
    def add_vacancy(vacancy):
        """Абстрактный метод, который должен быть переопределен в дочерных классах родительского класса Adder."""
        pass


class CSVSaver(Adder):
    """Класс для работы с данными в файле в формате csv."""

    @staticmethod
    def add_vacancy(vacancy):
        """
        Метод добавляет в файл в формате csv вакансию, информация об которой указана в vacancy. Передававаемый
        аргумент должен быть экземпляром класса Vacancy, иначе возникнет исключение TypeError.
        """

        if not isinstance(vacancy, Vacancy):
            raise TypeError('Передаваемый аргумент должен быть экземпляром класса Vacancy.')
        with open('db_vacancies.csv', 'a', newline='', encoding='UTF-16') as file:
            if os.stat('db_vacancies.csv').st_size == 0:
                writer = csv.writer(file, delimiter='\t')
                head_row = ('Идентификатор', 'Название_вакансии', 'Ссылка', 'Зарплата_от', 'Зарплата_до',
                            'Имя_нанимателя', 'Город', 'Описание_вакансии', 'Требование', 'Опыт', 'Дата_публикации')
                writer.writerow(head_row)