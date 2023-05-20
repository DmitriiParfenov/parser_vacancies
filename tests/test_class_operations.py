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


def test_vacancy_get_id(vacancies_examples):
    result = []
    for elem in vacancies_examples:
        result.append(elem.id)
    assert result == [1, 2, 3, 4, 5]


def test_vacancy_get_url(vacancies_examples):
    result = []
    for elem in vacancies_examples:
        result.append(elem.url)
    assert result == ['https://example1.ru/', 'https://example2.ru/', 'https://example3.ru/', 'https://example4.ru/',
                      'https://example5.ru/']


@pytest.mark.parametrize("inner_index, outer_index, expected", [(0, 0, 'Идентификатор вакансии — 1'),
                                                                (1, 1, 'title — Биоинформатик'),
                                                                (2, 4, 'Ссылка на вакансию — https://example5.ru/'),
                                                                (3, 2, 'salary_from — None'),
                                                                (4, 3, 'salary_to — 250000'),
                                                                (5, 4, 'name_employer — BIOCAD'),
                                                                (6, 0, 'city — Санкт-Петербург'),
                                                                (7, 3, 'description — Описание_4'),
                                                                (8, 1, 'requirement — Программирование'),
                                                                (9, 1, 'experience — От 1 года до 3 лет'),
                                                                (10, 4, 'date — 2023-01-05 00:00:00'),
                                                                ])
def test_vacancy_method__str__(vacancies_examples, inner_index, outer_index, expected):
    test_object = vacancies_examples[outer_index]
    result = str(test_object).split('\n')
    assert result[inner_index] == expected


def test_vacancy_method__repr__(vacancies_examples):
    assert repr(vacancies_examples[0]) == (
        "Vacancy(1, 'Биоинформатик', 'https://example1.ru/', 30000, 60000, 'BIOCAD', "
        "'Санкт-Петербург', 'Описание_1', 'Секвенирование','Нет опыта работы', "
        '2023-01-01 00:00:00)')


@pytest.mark.parametrize("expected, inner_index, argument", [(ValueError, 0, 10), (ValueError, 1, 15),
                                                             (ValueError, 4, 20), (ValueError, 2, -100)])
def test_vacancy_method__eq__1(vacancies_examples, expected, inner_index, argument):
    with pytest.raises(expected):
        result = vacancies_examples[inner_index] == argument


@pytest.mark.parametrize("index_1, index_2, expected", [(0, 1, False), (4, 3, True), (2, 3, False),
                                                        (3, 4, True), (2, 2, True)])
def test_vacancy_method__eq__2(vacancies_examples, index_1, index_2, expected):
    assert (vacancies_examples[index_1] == vacancies_examples[index_2]) == expected


@pytest.mark.parametrize("expected, inner_index, argument", [(ValueError, 0, 10), (ValueError, 1, 15),
                                                             (ValueError, 4, 20), (ValueError, 2, -100)])
def test_vacancy_method__compare__1(vacancies_examples, expected, inner_index, argument):
    with pytest.raises(expected):
        result = vacancies_examples[inner_index] > argument


@pytest.mark.parametrize("expected, inner_index, argument", [(ValueError, 2, 10), (ValueError, 3, 15),
                                                             (ValueError, 4, 20), (ValueError, 1, -100)])
def test_vacancy_method__compare__2(vacancies_examples, expected, inner_index, argument):
    with pytest.raises(expected):
        result = vacancies_examples[inner_index] >= argument


@pytest.mark.parametrize("index_1, index_2, expected", [(0, 1, False), (0, 2, True), (2, 3, False),
                                                        (3, 2, True), (1, 1, False), (1, 4, False)])
def test_vacancy_method__compare__3(vacancies_examples, index_1, index_2, expected):
    assert (vacancies_examples[index_1] > vacancies_examples[index_2]) == expected


@pytest.mark.parametrize("index_1, index_2, expected", [(0, 1, False), (0, 2, True), (2, 3, False),
                                                        (3, 2, True), (1, 1, True), (1, 4, False)])
def test_vacancy_method__compare__3(vacancies_examples, index_1, index_2, expected):
    assert (vacancies_examples[index_1] >= vacancies_examples[index_2]) == expected


@pytest.mark.parametrize("index_1, index_2, expected", [(1, 0, False), (4, 0, False), (3, 1, False),
                                                        (2, 0, True), (1, 1, False), (2, 4, True)])
def test_vacancy_method__compare__4(vacancies_examples, index_1, index_2, expected):
    assert (vacancies_examples[index_1] < vacancies_examples[index_2]) == expected

