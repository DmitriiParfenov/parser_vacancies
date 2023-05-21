import datetime
from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для работы с API сервераов с вакансиями."""

    @abstractmethod
    def get_vacancies(self, title_vacancy):
        """Абстрактный метод, который должен быть переопределен в дочерных классах родительского класса Parser."""
        pass