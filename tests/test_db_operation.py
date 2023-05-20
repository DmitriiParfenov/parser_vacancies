from datetime import datetime as dt

import pytest

from utils.db_operation import CSVSaver, Adder


def test_subclasses_csv_saver():
    assert issubclass(CSVSaver, Adder) is True
