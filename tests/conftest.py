import csv
from datetime import datetime as dt

import pytest

from utils.class_operations import Vacancy
from utils.db_operation import CSVSaver


@pytest.fixture
def vacancies_examples():
    vacancies = [Vacancy(1, 'Биоинформатик', 'https://example1.ru/', 30000, 60000, 'BIOCAD', 'Санкт-Петербург',
                         'Описание_1', 'Секвенирование', 'Нет опыта работы', dt(2023, 1, 1)),
                 Vacancy(2, 'Биоинформатик', 'https://example2.ru/', None, 100000, 'BIOCAD', 'Москва',
                         'Описание_2', 'Программирование', 'От 1 года до 3 лет', dt(2023, 1, 2)),
                 Vacancy(3, 'Менеджер', 'https://example3.ru/', None, None, 'BIOCAD', 'Воронеж',
                         'Описание_3', 'Биоинформатик', 'От 3 до 6 лет', dt(2023, 1, 3)),
                 Vacancy(4, 'биоинформатик', 'https://example4.ru/', None, 250000, 'BIOCAD', 'Воронеж',
                         'Описание_4', 'Анализ данных', 'От 3 до 6 лет', dt(2023, 1, 4)),
                 Vacancy(5, 'биоинформатик', 'https://example5.ru/', None, 250000, 'BIOCAD', 'Санкт-Петербург',
                         'Описание_5', 'Pipelines', 'Более 6 лет', dt(2023, 1, 5))
                 ]
    return vacancies


@pytest.fixture
def get_instance_saver():
    return CSVSaver()


@pytest.fixture
def get_empty_file():
    with open('db_vacancies.csv', 'w', newline='', encoding='UTF-16'):
        pass


@pytest.fixture
def get_file_with_two_rows(vacancies_examples):
    with open('db_vacancies.csv', 'w', newline='', encoding='UTF-16') as file:
        writer = csv.writer(file, delimiter='\t')
        head_row = ('Идентификатор', 'Название_вакансии', 'Ссылка', 'Зарплата_от', 'Зарплата_до',
                    'Имя_нанимателя', 'Город', 'Описание_вакансии', 'Требование', 'Опыт', 'Дата_публикации')
        writer.writerow(head_row)
        data_row = (vacancies_examples[0].id, vacancies_examples[0].title, vacancies_examples[0].url,
                    vacancies_examples[0].salary_from,
                    vacancies_examples[0].salary_to, vacancies_examples[0].name_employer,
                    vacancies_examples[0].city, vacancies_examples[0].description,
                    vacancies_examples[0].requirement, vacancies_examples[0].experience, vacancies_examples[0].date)
        writer.writerow(data_row)
