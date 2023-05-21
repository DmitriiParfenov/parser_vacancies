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
