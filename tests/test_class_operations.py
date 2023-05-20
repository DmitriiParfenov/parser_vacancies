from datetime import datetime as dt

import pytest

from utils.class_operations import Vacancy


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


@pytest.mark.parametrize("expected, id_, title, url, salary_from, salary_to, name, city, desc, req, exp, date",
                         [(TypeError, '1', 'title', 'https://ex.ru', 3, 5, 'name', 'city', 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 1, 'https://ex.ru', 3, 5, 'name', 'city', 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', {'a': 1}, 3, 5, 'name', 'city', 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'str', 3, 5, 'name', 'city', 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', '3', 5, 'name', 'city', 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', 3, '5', 'name', 'city', 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', 3, 5, {'name'}, 'city', 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', 3, 5, 'name', {'city'}, 'desc', 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', 3, 5, 'name', 'city', 2.6, 'req', 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', 3, 5, 'name', 'city', 'desc', {'req'}, 'exp',
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', 3, 5, 'name', 'city', 'desc', 'req', 1,
                           dt(2023, 1, 1)),
                          (TypeError, 1, 'title', 'https://ex.ru', 3, 5, 'name', 'city', 'desc', 'req', 1,
                           '2020-01-01')])
def test_vacancy_validate_data_1(id_, title, url, salary_from, salary_to, name, city, desc, req, exp, date, expected):
    with pytest.raises(expected):
        Vacancy(id_, title, url, salary_from, salary_to, name, city, desc, req, exp, date)


def test_vacancy_validate_data_2(vacancies_examples):
    result = []
    for elem in vacancies_examples:
        result.append(isinstance(elem, Vacancy))
    assert result == [True, True, True, True, True]
