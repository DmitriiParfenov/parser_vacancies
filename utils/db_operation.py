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

        with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as read_to_file:
            reader = csv.DictReader(read_to_file, delimiter='\t')
            data = [x.get('Ссылка') for x in reader]
            if vacancy.url not in data:
                with open('db_vacancies.csv', 'a', newline='', encoding='UTF-16') as add_to_file:
                    writer = csv.writer(add_to_file, delimiter='\t')
                    info_from_vacancy = (vacancy.id, vacancy.title, vacancy.url, vacancy.salary_from,
                                         vacancy.salary_to, vacancy.name_employer,
                                         vacancy.city, vacancy.description,
                                         vacancy.requirement, vacancy.experience, vacancy.date)
                    writer.writerow(info_from_vacancy)

    @staticmethod
    def get_vacancies_by_salary(salary_amount, date=None):
        """Метод вернет те вакансии из csv-файла, у которых диапазон зарплаты включает зарплатные ожидания кандидата."""

        if os.stat('db_vacancies.csv').st_size > 1:
            with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
                reader = csv.DictReader(file, delimiter='\t')
                vacancy_sorted_by_salary = []
                data = [x for x in reader if x.get('Зарплата_от') or x.get('Зарплата_до')]
                for vacancy in data:
                    if vacancy.get('Зарплата_от') and vacancy.get('Зарплата_до'):
                        if int(vacancy.get('Зарплата_от')) >= salary_amount or \
                                salary_amount <= int(vacancy.get('Зарплата_до')):
                            vacancy_sorted_by_salary.append(vacancy)
                    elif vacancy.get('Зарплата_от'):
                        if int(vacancy.get('Зарплата_от')) >= salary_amount:
                            vacancy_sorted_by_salary.append(vacancy)
                    elif vacancy.get('Зарплата_до'):
                        if int(vacancy.get('Зарплата_до')) >= salary_amount:
                            vacancy_sorted_by_salary.append(vacancy)
                if date:
                    vacancy_sorted_by_salary.sort(key=lambda x: x['Дата_публикации'], reverse=True)
            return vacancy_sorted_by_salary
        else:
            return f'В базе данных еще нет ни одной вакансии'