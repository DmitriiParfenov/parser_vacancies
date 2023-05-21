import csv

import pytest

from utils.db_operation import CSVSaver, Adder


def test_subclasses_csv_saver():
    assert issubclass(CSVSaver, Adder) is True


@pytest.mark.parametrize("expected, argument", [(TypeError, '1'), (TypeError, 250), (TypeError, {'a': 1})])
def test_add_incorrect_data_to_file(get_instance_saver, expected, argument):
    with pytest.raises(expected):
        get_instance_saver.add_vacancy(argument)


def test_add_data_to_empty_file(get_empty_file, get_instance_saver, vacancies_examples):
    get_instance_saver.add_vacancy(vacancies_examples[0])
    with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
        reader = csv.reader(file, delimiter='\t')
        data = [row for row in reader]
    assert data[0] == ['Идентификатор', 'Название_вакансии', 'Ссылка', 'Зарплата_от', 'Зарплата_до',
                       'Имя_нанимателя', 'Город', 'Описание_вакансии', 'Требование', 'Опыт', 'Дата_публикации']


def test_check_count_headers(get_file_with_two_rows, vacancies_examples, get_instance_saver):
    get_instance_saver.add_vacancy(vacancies_examples[1])
    result = 0
    with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
        reader = csv.reader(file, delimiter='\t')
        for item in reader:
            if item[0] == 'Идентификатор':
                result += 1
    assert result == 1


def test_unique_data_in_file(get_file_with_two_rows, vacancies_examples, get_instance_saver):
    get_instance_saver.add_vacancy(vacancies_examples[0])
    with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
        reader = csv.reader(file, delimiter='\t')
        unique = sum([1 for x in reader])
    assert unique == 2


@pytest.mark.parametrize("argument, expected", [(30000, ['1', '2', '4', '5']),
                                                (250000, ['4', '5']), (500000, [])])
def test_get_vacancies_by_salary(get_instance_saver, get_file_with_data, argument, expected):
    vac = get_instance_saver.get_vacancies_by_salary(argument)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("argument_1, argument_2, expected", [(30000, True, ['5', '4', '2', '1']),
                                                              (250000, True, ['5', '4']),
                                                              (250000, False, ['4', '5'])])
def test_get_vacancies_by_salary_and_date(get_instance_saver, get_file_with_data,
                                          argument_1, argument_2, expected):
    vac = get_instance_saver.get_vacancies_by_salary(argument_1, argument_2)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


def test_get_vacancies_by_salary_from_empty_file(get_instance_saver, get_empty_file):
    vac = get_instance_saver.get_vacancies_by_salary(50000)
    assert vac == 'В базе данных еще нет ни одной вакансии'


@pytest.mark.parametrize("argument, expected", [('Нет опыта работы', ['1']), ('Более 6 лет', ['5']),
                                                ('От 1 года до 3 лет', ['2']), ('От 3 до 6 лет', ['3', '4'])])
def test_get_vacancies_by_experience(get_instance_saver, get_file_with_data, argument, expected):
    vac = get_instance_saver.get_vacancies_by_experience(argument)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, expected", [('От 3 до 6 лет', True, ['4', '3']),
                                                    ('От 3 до 6 лет', False, ['3', '4'])])
def test_get_vacancies_by_experience_and_date(get_instance_saver, get_file_with_data, arg_1, arg_2, expected):
    vac = get_instance_saver.get_vacancies_by_experience(arg_1, arg_2)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


def test_get_vacancies_by_experience_from_empty_file(get_instance_saver, get_empty_file):
    vac = get_instance_saver.get_vacancies_by_experience('От 3 до 6 лет')
    assert vac == 'В базе данных еще нет ни одной вакансии'


@pytest.mark.parametrize("argument, expected", [('Санкт-Петербург', ['1', '5']), ('Воронеж', ['3', '4']),
                                                ('москва', ['2']), ('Самара', [])])
def test_get_vacancies_by_city(get_instance_saver, get_file_with_data, argument, expected):
    vac = get_instance_saver.get_vacancies_by_city(argument)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg1, arg2, expected", [('Санкт-Петербург', True, ['5', '1']), ('воронеж', True, ['4', '3']),
                                                  ('Санкт-Петербург', False, ['1', '5']),
                                                  ('Воронеж', False, ['3', '4'])])
def test_get_vacancies_by_city_and_date(get_instance_saver, get_file_with_data, arg1, arg2, expected):
    vac = get_instance_saver.get_vacancies_by_city(arg1, arg2)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


def test_get_vacancies_by_city_from_empty_file(get_instance_saver, get_empty_file):
    vac = get_instance_saver.get_vacancies_by_city('москва')
    assert vac == 'В базе данных еще нет ни одной вакансии'


@pytest.mark.parametrize("arg_1, arg_2, expected", [(30000, 'Нет опыта работы', ['1']),
                                                    (150000, 'От 3 до 6 лет', ['4']),
                                                    (30000, 'От 3 до 6 лет', ['4']),
                                                    (250000, 'Более 6 лет', ['5']),
                                                    (100000, 'Нет опыта', [])])
def test_get_vacancy_by_experience_and_salary(get_instance_saver, get_file_with_data, arg_1, arg_2, expected):
    vac = get_instance_saver.get_vacancy_by_experience_and_salary(arg_1, arg_2)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, expected", [('Нет опыта работы', 'Санкт-Петербург', ['1']),
                                                    ('Более 6 лет', 'санкт-петербург', ['5']),
                                                    ('Нет опыта работы', 'Воронеж', []),
                                                    ('От 3 до 6 лет', 'Санкт-Петербург', []),
                                                    ('От 3 до 6 лет', 'Воронеж', ['3', '4'])])
def test_get_vacancy_by_experience_and_city(get_instance_saver, get_file_with_data, arg_1, arg_2, expected):
    vac = get_instance_saver.get_vacancy_by_experience_and_city(arg_1, arg_2)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, arg_3, expected", [('Нет опыта работы', 'Воронеж', True, []),
                                                           ('От 3 до 6 лет', 'Санкт-Петербург', True, []),
                                                           ('От 3 до 6 лет', 'Воронеж', False, ['3', '4']),
                                                           ('От 3 до 6 лет', 'Воронеж', True, ['4', '3'])])
def test_get_vacancy_by_experience_city_and_date(get_instance_saver, get_file_with_data, arg_1, arg_2, arg_3, expected):
    vac = get_instance_saver.get_vacancy_by_experience_and_city(arg_1, arg_2, arg_3)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, arg_3, expected", [(30000, 'Нет опыта работы', 'Санкт-Петербург', ['1']),
                                                           (100000, 'Более 6 лет', 'санкт-петербург', ['5']),
                                                           (500000, 'Нет опыта работы', 'Воронеж', []),
                                                           (100000, 'От 3 до 6 лет', 'Санкт-Петербург', []),
                                                           (200000, 'От 3 до 6 лет', 'Воронеж', ['4'])])
def test_get_vacancy_by_experience_salary_and_city(get_instance_saver, get_file_with_data,
                                                   arg_1, arg_2, arg_3, expected):
    vac = get_instance_saver.get_vacancy_by_experience_salary_and_city(arg_1, arg_2, arg_3)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, expected", [(10000, 'Санкт-Петербург', ['1', '5']),
                                                    (200000, 'Воронеж', ['4']),
                                                    (20000, 'Воронеж', ['4']),
                                                    (500000, 'Санкт-Петербург', []),
                                                    (50000, 'Москва', ['2'])])
def test_get_vacancy_by_salary_and_city(get_instance_saver, get_file_with_data, arg_1, arg_2, expected):
    vac = get_instance_saver.get_vacancy_by_salary_and_city(arg_1, arg_2)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, arg_3, expected", [(10000, 'Санкт-Петербург', True, ['5', '1']),
                                                           (10000, 'Санкт-Петербург', False, ['1', '5'])])
def test_get_vacancy_by_salary_city_and_date(get_instance_saver, get_file_with_data, arg_1, arg_2, arg_3, expected):
    vac = get_instance_saver.get_vacancy_by_salary_and_city(arg_1, arg_2, arg_3)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, arg_3, expected", [(10000, 'Нет опыта работы', 'Санкт-Петербург', ['1']),
                                                           (False, 'Нет опыта работы', 'Санкт-Петербург', ['1']),
                                                           (10000, 'Более 6 лет', 'Санкт-Петербург', ['5']),
                                                           (10000, False, 'Санкт-Петербург', ['1', '5']),
                                                           (10000, 'Более 6 лет', False, ['5']),
                                                           (10000, False, False, ['1', '2', '4', '5']),
                                                           (100000, False, False, ['2', '4', '5']),
                                                           (100000, 'Нет опыта работы', 'Москва', []),
                                                           (False, False, False, ['1', '2', '3', '4', '5']),
                                                           (False, 'Нет опыта работы', False, ['1']),
                                                           (False, 'От 3 до 6 лет', False, ['3', '4']),
                                                           (False, False, 'Санкт-Петербург', ['1', '5']),
                                                           (False, False, 'Воронеж', ['3', '4']),
                                                           (False, False, 'Самара', []),
                                                           ])
def test_get_vacancy_by_filtered_words_not_in_title(get_instance_saver, get_file_with_data,
                                                    arg_1, arg_2, arg_3, expected):
    vac = get_instance_saver.get_vacancy_by_filtered_words_not_in_title(arg_1, arg_2, arg_3)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("a_1, a_2, a_3, a_4, expected", [(10000, False, 'Санкт-Петербург', True, ['5', '1']),
                                                          (10000, False, 'Санкт-Петербург', False, ['1', '5']),
                                                          (10000, False, False, True, ['5', '4', '2', '1']),
                                                          (10000, False, False, False, ['1', '2', '4', '5']),
                                                          (100000, False, False, True, ['5', '4', '2']),
                                                          (100000, False, False, False, ['2', '4', '5']),
                                                          (False, False, False, False, ['1', '2', '3', '4', '5']),
                                                          (False, False, False, True, ['5', '4', '3', '2', '1'])])
def test_get_vacancy_by_filtered_words_not_in_title_by_date(get_instance_saver, get_file_with_data,
                                                            a_1, a_2, a_3, a_4, expected):
    vac = get_instance_saver.get_vacancy_by_filtered_words_not_in_title(a_1, a_2, a_3, a_4)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


def test_get_vacancy_by_filtered_words_not_in_title_from_empty_file(get_instance_saver, get_empty_file):
    vac = get_instance_saver.get_vacancy_by_filtered_words_not_in_title(10000, False, 'Санкт-Петербург')
    assert vac == 'В базе данных еще нет ни одной вакансии'


def test_get_vacancy_by_date(get_instance_saver, get_file_with_data):
    vac = get_instance_saver.get_vacancy_by_date()
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == ['5', '4', '3', '2', '1']


def test_get_vacancy_by_date_from_empty_file(get_instance_saver, get_empty_file):
    vac = get_instance_saver.get_vacancy_by_date()
    assert vac == 'В базе данных еще нет ни одной вакансии'


@pytest.mark.parametrize("arg_1, arg_2, arg_3, arg_4, expected",
                         [('биоинформатик', 10000, 'Нет опыта работы', 'Санкт-Петербург', ['1']),
                          ('менеджер', 10000, 'Нет опыта работы', 'Санкт-Петербург', []),
                          ('биоинформатик', 250000, False, False, ['4', '5']),
                          ('стажер', 100000, False, False, []),
                          ('биоинформатик', False, 'Нет опыта работы', False, ['1']),
                          ('менеджер', False, 'От 3 до 6 лет', False, ['3']),
                          ('Ученый', False, 'Нет опыта работы', False, []),
                          ('биоинформатик', 30000, False, 'Санкт-Петербург', ['1', '5']),
                          ('менеджер', 30000, False, 'Воронеж', []),
                          ('биоинформатик', 30000, False, 'Москва', ['2']),
                          ('биоинформатик', False, False, 'Москва', ['2']),
                          ('биоинформатик', False, False, 'Воронеж', ['4']),
                          ('биоинформатик', False, False, 'Самара', []),
                          ('менеджер', False, False, 'Воронеж', ['3']),
                          ('биоинформатик', 50000, 'Нет опыта работы', False, ['1']),
                          ('биоинформатик', 50000, 'Более 6 лет', False, ['5']),
                          ('менеджер', 50000, 'Нет опыта работы', False, []),
                          ('биоинформатик', False, 'От 3 до 6 лет', 'Воронеж', ['4']),
                          ('менеджер', False, 'От 3 до 6 лет', 'Воронеж', ['3']),
                          ('биоинформатик', False, 'Нет опыта работы', 'Санкт-Петербург', ['1']),
                          ('биоинформатик', False, 'От 3 до 6 лет', 'Махачкала', []),
                          ('биоинформатик', False, False, False, ['1', '2', '4', '5']),
                          ('менеджер', False, False, False, ['3'])
                          ])
def test_get_vacancy_by_keyword_in_title(get_instance_saver, get_file_with_data, arg_1, arg_2, arg_3, arg_4, expected):
    vac = get_instance_saver.get_vacancy_by_keyword_in_title(arg_1, arg_2, arg_3, arg_4)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


@pytest.mark.parametrize("arg_1, arg_2, arg_3, arg_4, arg_5, expected",
                         [('биоинформатик', 250000, False, False, False, ['4', '5']),
                          ('биоинформатик', 250000, False, False, True, ['5', '4']),
                          ('биоинформатик', 30000, False, 'Санкт-Петербург', True, ['5', '1']),
                          ('биоинформатик', 30000, False, 'Санкт-Петербург', False, ['1', '5']),
                          ('биоинформатик', False, False, False, False, ['1', '2', '4', '5']),
                          ('биоинформатик', False, False, False, True, ['5', '4', '2', '1'])
                          ])
def test_get_vacancy_by_keyword_in_title_by_date(get_instance_saver, get_file_with_data,
                                                 arg_1, arg_2, arg_3, arg_4, arg_5, expected):
    vac = get_instance_saver.get_vacancy_by_keyword_in_title(arg_1, arg_2, arg_3, arg_4, arg_5)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected


def test_get_vacancy_by_keyword_in_title_from_empty_file(get_instance_saver, get_empty_file):
    vac = get_instance_saver.get_vacancy_by_keyword_in_title('биоинформатик', 250000, False, False, False)
    assert vac == 'В базе данных еще нет ни одной вакансии'


def test_delete_vacancy(get_instance_saver, get_file_with_data, get_single_vacancy):
    get_instance_saver.delete_vacancy(get_single_vacancy)
    with open('db_vacancies.csv', 'r', newline='', encoding='UTF-16') as file:
        reader = csv.reader(file, delimiter='\t')
        count_rows = sum(1 for x in reader)
    assert count_rows == 5


def test_delete_vacancy_validate_date(get_instance_saver, get_file_with_data):
    with pytest.raises(TypeError):
        get_instance_saver.delete_vacancy('vacancy')


def test_delete_vacancy_from_empty_file(get_instance_saver, get_empty_file, get_single_vacancy):
    res = get_instance_saver.delete_vacancy(get_single_vacancy)
    assert res == 'В базе данных еще нет ни одной вакансии'