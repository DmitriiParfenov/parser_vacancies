import pytest

from utils.db_operation import CSVSaver, Adder


def test_subclasses_csv_saver():
    assert issubclass(CSVSaver, Adder) is True


@pytest.mark.parametrize("expected, argument", [(TypeError, '1'), (TypeError, 250), (TypeError, {'a': 1})])
def test_add_incorrect_data_to_file(get_instance_saver, expected, argument):
    with pytest.raises(expected):
        get_instance_saver.add_vacancy(argument)
