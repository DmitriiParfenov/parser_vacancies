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
