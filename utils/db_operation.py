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

    @staticmethod
    def get_vacancies_by_experience(experience, date=None):
        """Метод вернет вакансии из csv-файла по фильтру <experience> (опыт работы)."""

        if os.stat('db_vacancies.csv').st_size > 1:
            with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
                reader = csv.DictReader(file, delimiter='\t')
                vacancy_by_experience = []
                data = [x for x in reader if x.get('Опыт')]
                for vacancy in data:
                    if vacancy.get('Опыт') == experience:
                        vacancy_by_experience.append(vacancy)
            if date:
                vacancy_by_experience.sort(key=lambda x: x['Дата_публикации'], reverse=True)
            return vacancy_by_experience
        else:
            return f'В базе данных еще нет ни одной вакансии'

    @staticmethod
    def get_vacancies_by_city(city, date=None):
        """Метод вернет вакансии из csv-файла по фильтру <city> (город)."""

        if os.stat('db_vacancies.csv').st_size > 1:
            with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
                reader = csv.DictReader(file, delimiter='\t')
                vacancy_by_city = []
                data = [x for x in reader if x.get('Город')]
                for vacancy in data:
                    if vacancy.get('Город').lower() == city.lower():
                        vacancy_by_city.append(vacancy)
            if date:
                vacancy_by_city.sort(key=lambda x: x['Дата_публикации'], reverse=True)
            return vacancy_by_city
        else:
            return f'В базе данных еще нет ни одной вакансии'

    @classmethod
    def get_vacancy_by_experience_and_salary(cls, salary, experience, date=None):
        """Метод вернет вакансии из csv-файла по фильтру <experience> (опыт работы) и <salary> (зарплата)."""

        vacancies = [x for x in cls.get_vacancies_by_salary(salary) if x in cls.get_vacancies_by_experience(experience)]
        if date:
            vacancies.sort(key=lambda x: x['Дата_публикации'], reverse=True)
        return vacancies

    @classmethod
    def get_vacancy_by_experience_salary_and_city(cls, salary, experience, city, date=None):
        """Метод вернет вакансии из csv-файла по фильтру <experience> (опыт работы), <salary> (зарплата) и
        <city> (город)."""

        vacancies = [x for x in cls.get_vacancy_by_experience_and_salary(salary, experience)
                     if x in cls.get_vacancies_by_city(city)]
        if date:
            vacancies.sort(key=lambda x: x['Дата_публикации'], reverse=True)
        return vacancies

    @classmethod
    def get_vacancy_by_experience_and_city(cls, experience, city, date=None):
        """Метод вернет вакансии из csv-файла по фильтру <experience> (опыт работы) и <city> (город)."""

        vacancies = [x for x in cls.get_vacancies_by_experience(experience) if x in cls.get_vacancies_by_city(city)]
        if date:
            vacancies.sort(key=lambda x: x['Дата_публикации'], reverse=True)
        return vacancies

    @classmethod
    def get_vacancy_by_salary_and_city(cls, salary, city, date=None):
        """Метод вернет вакансии из csv-файла по фильтру <salary> (зарплата) и <city> (город)."""

        vacancies = [x for x in cls.get_vacancies_by_salary(salary) if x in cls.get_vacancies_by_city(city)]
        if date:
            vacancies.sort(key=lambda x: x['Дата_публикации'], reverse=True)
        return vacancies

    @classmethod
    def get_vacancy_by_filtered_words_not_in_title(cls, salary=None, experience=None, city=None, date=None):
        """
        Метод вернет вакансии по ключевому слову по всей вакансии из csv-файла по заданным фильтрам, указанными
        в аргументах метода:
        <salary> (зарплаты) — если указан,
        <experience> (опыт работы) — если указан,
        <city> (город) — если указан,
        <date> (сортировка вывода) — если указан.
        """

        if os.stat('db_vacancies.csv').st_size > 1:
            with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
                reader = csv.DictReader(file, delimiter='\t')
                data = [x for x in reader]
                result_vacancies = []
                if salary and not experience and not city:
                    result_vacancies = [x for x in cls.get_vacancies_by_salary(salary) if x in data]
                elif experience and not salary and not city:
                    result_vacancies = [x for x in cls.get_vacancies_by_experience(experience) if x in data]
                elif city and not experience and not salary:
                    result_vacancies = [x for x in cls.get_vacancies_by_city(city) if x in data]
                elif salary and city and not experience:
                    result_vacancies = [x for x in cls.get_vacancy_by_salary_and_city(salary, city) if x in data]
                elif salary and experience and not city:
                    result_vacancies = [x for x in cls.get_vacancy_by_experience_and_salary(salary, experience)
                                        if x in data]
                elif salary and experience and city:
                    result_vacancies = [x for x in
                                        cls.get_vacancy_by_experience_salary_and_city(salary, experience, city)
                                        if x in data]
                elif experience and city and not salary:
                    result_vacancies = [x for x in cls.get_vacancy_by_experience_and_city(experience, city)
                                        if x in data]
                elif not salary and not experience and not city:
                    result_vacancies = data
                if date:
                    result_vacancies.sort(key=lambda x: x['Дата_публикации'], reverse=True)
                return result_vacancies
        else:
            return f'В базе данных еще нет ни одной вакансии'