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
                                                (250000, ['4', '5'])])
def test_get_vacancies_by_salary(vacancies_examples, get_instance_saver, get_file_with_data, argument, expected):
    vac = get_instance_saver.get_vacancies_by_salary(argument)
    result = list()
    for item in vac:
        result.append(item.get('Идентификатор'))
    assert result == expected
